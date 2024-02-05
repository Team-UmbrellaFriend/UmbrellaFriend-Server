#users/customAuth.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, studentID = None, password = None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(profile__studentID = studentID)
        except User.DoesNotExist:
            return None

        stored_password = user.password
        if check_password(password, stored_password):
            return user

        return None