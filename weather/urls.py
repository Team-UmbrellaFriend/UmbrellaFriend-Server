#weather/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('rain/', get_rain_percent),
]