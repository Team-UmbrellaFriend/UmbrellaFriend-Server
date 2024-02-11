#users/serializers.py
from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # Django의 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구

from django.contrib.auth import authenticate # DefautlAuthBackend인 TokenAuth 방식으로 유저 인증
from .models import Profile


# 회원가입
class SignUpProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source = 'user.id', read_only = True)
    class Meta:
        model = Profile
        fields = ('user_id', 'studentID', 'studentCard', 'phoneNumber')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset = User.objects.all())],
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

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'profile')

    def validate(self, data):
        if (data['password'] != data['password2']):
            raise serializers.ValidationError(
                {"password": "Password fields did not match."})
        return data

    def create(self, validated_data): # 오버라이딩
        user = User.objects.create_user(
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
        )
        token = Token.objects.create(user = user)
        return {'token': token.key}


# 로그인
class LoginSerializer(serializers.Serializer):
    studentID = serializers.IntegerField(required = True)
    password = serializers.CharField(required = True, write_only = True)
    # write_only=True 옵션을 통해 클라이언트 -> 서버의 역직렬화는 가능하지만, 서버 -> 클라이언트 방향의 직렬화는 불가능하게 함

    def validate(self, data):
        studentID = data.get('studentID')
        password = data.get('password')

        user = authenticate(studentID = studentID, password = password)
        if user:
            token, is_created = Token.objects.get_or_create(user = user)
            return token
        raise serializers.ValidationError( # 가입된 유저가 없을 경우
            {"error": "Unable to log in with provided credentials."})


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
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'profile')


    def validate(self, data):
        email = data.get('email', None)
        if email and User.objects.exclude(pk=self.instance.pk).filter(email = email).exists():
            raise serializers.ValidationError('This email is already in use.')

        password = data.get('password', None)
        password2 = data.get('password2', None)
        print(password)
        print(password2)
        if password and password2 and password != password2:
            raise serializers.ValidationError('Passwords do not match.')
        return data


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile = instance.profile
        if profile_data:
            profile.studentID = profile_data.get('studentID', profile.studentID)
            profile.phoneNumber = profile_data.get('phoneNumber', profile.phoneNumber)
            profile.save()
        return instance