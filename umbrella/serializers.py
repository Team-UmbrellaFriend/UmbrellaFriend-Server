#umbrella/serializers.py
from rest_framework import serializers
from .models import Umbrella
from django.contrib.auth.models import User


class UmbrellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Umbrella
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'