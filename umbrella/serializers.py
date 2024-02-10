#umbrella/serializers.py
from rest_framework import serializers
from .models import Umbrella, Rent
from django.contrib.auth.models import User


class UmbrellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Umbrella
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    rent_date = serializers.DateTimeField(format = "%Y년%m월%d일")
    class Meta:
        model = Rent
        fields = ['rental_period', 'rent_date']