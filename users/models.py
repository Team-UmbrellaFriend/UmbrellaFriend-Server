#users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name='profile')
    # primary_key를 User의 pk로 설정하여 통합적으로 관리
    studentID = models.IntegerField(default = 0, unique = True)
    studentCard = models.ImageField(upload_to = 'media/')
    phoneNumber = models.CharField(max_length = 20)

    # @receiver(post_save, sender = User)
    # def create_student_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user = instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()