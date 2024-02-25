#mypage/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile
from umbrella.models import Rent

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('studentID', 'phoneNumber')


class MyRentSerializer(serializers.ModelSerializer):
    rent_date = serializers.DateTimeField(format = "%Y년 %m월 %d일", read_only = True)
    rental_period = serializers.CharField(max_length = 10, read_only = True)

    class Meta:
        model = Rent
        fields = ('rental_period', 'rent_date')