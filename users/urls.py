#users/urls.py
from django.urls import path
from .views import SignUpView, LoginView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]