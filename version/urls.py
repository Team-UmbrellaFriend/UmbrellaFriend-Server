#version/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('get_version_info/', get_version_info),
]