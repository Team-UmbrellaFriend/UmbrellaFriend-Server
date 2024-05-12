#users/models.py
from django.db import models
from umbrella.models import Umbrella
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 10, unique = False)
    email = models.EmailField(unique = True)
    
    USERNAME_FIELD = 'email'  # email 필드를 USERNAME_FIELD로 설정
    REQUIRED_FIELDS = ['username']  # email을 제외한 필수 필드 목록
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True, related_name = 'profile')
    studentID = models.IntegerField(default = 0, unique = True)
    studentCard = models.ImageField(upload_to = f'profile')
    phoneNumber = models.CharField(max_length = 20)
    umbrella = models.OneToOneField(Umbrella, related_name = 'user', null = True, blank = True, on_delete = models.SET_NULL)
    fcm_token = models.CharField(max_length = 200, blank = True, null = True)


class WithdrawalRecord(models.Model):
    REPORT_CHOICES = (
        ('수량', '우산 수량이 적어서 사용을 잘 안해요.'),
        ('관리', '우산 관리가 잘 안되어 사용할 수 없어요.'),
        ('새계정', '새 계정을 만들고 싶어요.'),
        ('기타', '기타사항 (직접 입력)'),
    )
    
    studentID = models.IntegerField(default = 0, unique = True)
    withdrawal_reason = models.CharField(max_length = 10, choices = REPORT_CHOICES)
    description = models.TextField(max_length = 200, blank = True, null = True)
    withdrawal_date = models.DateTimeField(default = timezone.now)
    expiration_date = models.DateTimeField(default = lambda: timezone.now() + timezone.timedelta(days = 7)) # 만료 일자

    def __str__(self):
        return f'[{self.studentID}] {self.withdrawal_reason}'