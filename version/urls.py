#version/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('version/info/', get_version_info),
]