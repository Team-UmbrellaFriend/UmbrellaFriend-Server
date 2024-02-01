#users/serializers.py
from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # Django의 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구


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