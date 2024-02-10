#umbrella/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Umbrella(models.Model):
    number = models.IntegerField(unique = True)
    is_available = models.BooleanField(default = True)

    place = {
        '명신관': 1,
        '순헌관': 2,
        '학생회관': 3,
        '도서관': 4,
        '음대': 5,
        '백주년기념관': 6,
    }
    
    location = models.CharField(
        max_length = 20,
        choices = place,
        default = 4
    )
    
    def get_location_id(self, location):
        return int(self.place.get(location, 0))

    def __str__(self):
        return f'[{self.number}] Umbrella'


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    umbrella = models.ForeignKey(Umbrella, on_delete = models.CASCADE)
    rent_date = models.DateTimeField(default = timezone.now) # 대여 날짜
    return_date = models.DateTimeField(null = True, blank = True) # 반납 날짜
    return_due_date = models.DateTimeField(default = timezone.now() + timezone.timedelta(days = 3)) # 반납 기한
    rental_period = models.CharField(max_length = 10, null = True, blank = True) # 대여 기간

    def is_overdue(self):
        return timezone.now() > self.return_due_date

    def save(self, *args, **kwargs):
        # 대여 기간을 저장하기 전에 계산
        if self.return_date:
            period = self.return_date - self.rent_date
            self.rental_period = f'{period.days + 1}일간 대여'
        else:
            self.rental_period = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.user}] {self.umbrella}'