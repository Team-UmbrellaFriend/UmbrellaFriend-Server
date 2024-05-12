#users/urls.py
from django.urls import path
from .views import SignUpView, LoginView, LogoutView, ProfileView, DeleteAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/<int:user_id>/', ProfileView.as_view()),
    path('withdraw/', DeleteAccountView.as_view()),
]