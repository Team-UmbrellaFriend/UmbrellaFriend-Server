#users/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import SignUpSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer