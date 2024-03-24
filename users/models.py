#users/models.py
from django.db import models
from umbrella.models import Umbrella
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    username = models.CharField(max_length = 10, unique = False)
    email = models.EmailField(unique = True)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True, related_name = 'profile')
    studentID = models.IntegerField(default = 0, unique = True)
    studentCard = models.ImageField(upload_to = f'profile')
    phoneNumber = models.CharField(max_length = 20)
    umbrella = models.OneToOneField(Umbrella, related_name = 'user', null = True, blank = True, on_delete = models.SET_NULL)