#users/models.py
from django.db import models
from django.contrib.auth.models import User
from umbrella.models import Umbrella

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name = 'profile')
    studentID = models.IntegerField(default = 0, unique = True)
    studentCard = models.ImageField(upload_to = f'profile')
    phoneNumber = models.CharField(max_length = 20)
    umbrella = models.OneToOneField(Umbrella, related_name = 'user', null = True, blank = True, on_delete = models.SET_NULL)