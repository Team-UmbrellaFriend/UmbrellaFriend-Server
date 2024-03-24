#umbrella/serializers.py
from rest_framework import serializers
from .models import Rent
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    rent_date = serializers.DateTimeField(format = "%Y년%m월%d일", read_only = True)
    rental_period = serializers.CharField(max_length = 10, read_only = True)
    image = serializers.ImageField(required = False, allow_empty_file = True)

    class Meta:
        model = Rent
        fields = ['user', 'umbrella', 'rental_period', 'rent_date', 'image']