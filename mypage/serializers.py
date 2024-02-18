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
    rental_period = serializers.CharField(max_length = 10, read_only = True)

    class Meta:
        model = Rent
        fields = ('rental_period', 'rent_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        rent_date = instance.rent_date
        representation['rental_date'] = {
            'year': rent_date.year,
            'month': rent_date.month,
            'day': rent_date.day,
        }
        representation.pop('rent_date', None)
        return representation