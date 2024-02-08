#umbrella/admin.py
from django.contrib import admin
from .models import Umbrella, Rent

admin.site.register(Umbrella)
admin.site.register(Rent)