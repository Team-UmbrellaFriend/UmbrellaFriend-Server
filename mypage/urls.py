#mypage/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', MyPageView.as_view()),
    path('report/', report_umbrella),
]