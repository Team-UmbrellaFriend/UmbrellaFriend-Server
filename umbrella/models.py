#umbrella/models.py
from django.db import models

class Umbrella(models.Model):
    number = models.IntegerField(unique = True)
    is_available = models.BooleanField(default = True)

    def __str__(self):
        return f'[{self.number}] Umbrella'