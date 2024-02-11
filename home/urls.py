#home/urls.py
from django.urls import path
from .views import HomeView

urlpatterns = [
    path('info/', HomeView.as_view()),
]