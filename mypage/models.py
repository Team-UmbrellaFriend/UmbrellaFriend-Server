from django.db import models
from django.contrib.auth.models import User
from umbrella.models import Umbrella


class UmbrellaReport(models.Model):
    REPORT_CHOICES = (
        ('분실', '우산을 분실했어요'),
        ('QR', 'QR코드가 파손되었어요'),
        ('파손', '우산이 부러졌어요'),
        ('기타', '기타사항 (직접 입력)'),
    )

    umbrella = models.ForeignKey(Umbrella, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    report_reason = models.CharField(max_length=10, choices = REPORT_CHOICES)
    description = models.TextField(max_length = 200, blank = True, null = True)

    def __str__(self):
        return f'[{self.user.username}] 우산[{self.umbrella.number}] {self.report_reason}'