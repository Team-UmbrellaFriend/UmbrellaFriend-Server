#users/serializers.py
from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # Django의 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구

from django.contrib.auth import authenticate # DefautlAuthBackend인 TokenAuth 방식으로 유저 인증

# 회원가입
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())],
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

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

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
        # 유저 생성 및 토큰 생성
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user = user)
        return user


# 로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True, write_only = True)
    # write_only=True 옵션을 통해 클라이언트 -> 서버의 역직렬화는 가능하지만, 서버 -> 클라이언트 방향의 직렬화는 불가능하게 함

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user = user)
            return token
        raise serializers.ValidationError( # 가입된 유저가 없을 경우
            {"error": "Unable to log in with provided credentials."})