#users/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import SignUpSerializer, LoginSerializer, ProfileSerializer
from .models import Profile
from .permissions import CustomReadOnly

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response({'token': user_data['token']}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        token = serializer.validated_data # validate()의 리턴값인 token 받아오기
        return Response({"token": token.key}, status = status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def get(self, request, format = None):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]