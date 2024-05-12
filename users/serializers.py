#users/serializers.py
from django.contrib.auth.password_validation import validate_password # Django의 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구

from django.contrib.auth import authenticate # DefautlAuthBackend인 TokenAuth 방식으로 유저 인증
from django.contrib.auth.models import update_last_login
from .models import Profile, CustomUser, WithdrawalRecord

# 회원가입
class SignUpProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source = 'user.id', read_only = True)
    class Meta:
        model = Profile
        fields = ('user_id', 'studentID', 'studentCard', 'phoneNumber', 'fcm_token')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset = CustomUser.objects.all())],
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password], # 비밀번호 검증
    )
    password2 = serializers.CharField( # 비밀번호 2차 확인
        write_only = True,
        required = True,
    )
    profile = SignUpProfileSerializer()
    fcm_token = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'profile', 'fcm_token')

    def validate(self, data):
        if (data['password'] != data['password2']):
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data): # 오버라이딩
        fcm_token = validated_data.pop('fcm_token', None)
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        # 유저 생성
        user.set_password(validated_data['password'])
        user.save()

        # 프로필 정보 생성
        profile_data = validated_data.get('profile', {})
        Profile.objects.create(
            user = user,
            studentID = profile_data.get('studentID'),
            studentCard = profile_data.get('studentCard', None),
            phoneNumber = profile_data.get('phoneNumber', None),
            fcm_token = fcm_token
        )
        token = Token.objects.create(user = user)
        return {'token': token.key}


# 로그인
class LoginSerializer(serializers.Serializer):
    studentID = serializers.IntegerField(required = True)
    password = serializers.CharField(required = True, write_only = True)
    fcm_token = serializers.CharField(allow_blank=True, required=False)
    # write_only=True 옵션을 통해 클라이언트 -> 서버의 역직렬화는 가능하지만, 서버 -> 클라이언트 방향의 직렬화는 불가능하게 함

    def validate(self, data):
        studentID = data.get('studentID')
        password = data.get('password')
        fcm_token = data.get('fcm_token')

        user = authenticate(studentID = studentID, password = password)
        if user:
            token, is_created = Token.objects.get_or_create(user = user)
            if fcm_token:
                user.profile.fcm_token = fcm_token
                user.profile.save()
            update_last_login(None, user)
            return token
        raise serializers.ValidationError( # 가입된 유저가 없을 경우
            {"error": "가입된 유저가 없습니다."})


# 프로필
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('studentID', 'phoneNumber')

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        required = False,
        validators = [validate_password],
    )
    password2 = serializers.CharField(
        write_only = True,
        required = False,
    )
    profile = ProfileUpdateSerializer(partial = True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'profile')


    def validate(self, data):
        email = data.get('email', None)
        if email and CustomUser.objects.exclude(pk = self.instance.pk).filter(email = email).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일 주소입니다.')

        password = data.get('password', None)
        password2 = data.get('password2', None)
        if password and password2 and password != password2:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile = instance.profile
        if profile_data:
            profile.phoneNumber = profile_data.get('phoneNumber', profile.phoneNumber)
            profile.save()
        return instance



# 회원탈퇴
class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRecord
        fields = ('studentID', 'withdrawal_reason', 'description', 'withdrawal_date')