#mypage/urls.py
from django.urls import path
from .views import MyPageView

urlpatterns = [
    path('', MyPageView.as_view()),
]