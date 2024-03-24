from django.db import models
from django.conf import settings
from umbrella.models import Umbrella


class UmbrellaReport(models.Model):
    REPORT_CHOICES = (
        ('분실', '우산을 분실했어요'),
        ('QR', 'QR코드가 파손되었어요'),
        ('파손', '우산이 부러졌어요'),
        ('기타', '기타사항 (직접 입력)'),
    )

    umbrella = models.ForeignKey(Umbrella, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    report_reason = models.CharField(max_length = 10, choices = REPORT_CHOICES)
    description = models.TextField(max_length = 200, blank = True, null = True)
    is_done = models.BooleanField(default = False)

    def __str__(self):
        if self.is_done:
            return f'[{self.user.username}] 우산{self.umbrella.number} {self.report_reason} - 해결완료(O)'
        else:
            return f'[{self.user.username}] 우산{self.umbrella.number} {self.report_reason} - 해결안됨(X)'