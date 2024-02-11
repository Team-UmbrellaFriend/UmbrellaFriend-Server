#mypage/urls.py
from django.urls import path
from .views import MyPageView

urlpatterns = [
    path('info/', MyPageView.as_view()),
]