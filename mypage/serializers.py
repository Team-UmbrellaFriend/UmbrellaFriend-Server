#mypage/serializers.py
from rest_framework import serializers
from users.models import Profile, CustomUser
from umbrella.models import Rent
from .models import UmbrellaReport

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
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


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UmbrellaReport
        fields = ('user', 'umbrella', 'report_reason', 'description')