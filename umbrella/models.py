#umbrella/models.py
from django.db import models

class Umbrella(models.Model):
    number = models.IntegerField(unique = True)
    is_available = models.BooleanField(default = True)

    place = [
        ('명신관', '명신관'),
        ('순헌관', '순헌관'),
        ('학생회관', '학생회관'),
        ('도서관', '도서관')
    ]
    
    location = models.CharField(
        max_length = 20,
        choices = place,
        default = '도서관'
    )

    def __str__(self):
        return f'[{self.number}] Umbrella'