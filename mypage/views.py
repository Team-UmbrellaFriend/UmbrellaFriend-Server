from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from umbrella.models import Rent
from users.models import Profile
from .serializers import MyUserSerializer, MyProfileSerializer, MyRentSerializer
from datetime import *
from django.utils import timezone


def rent_history_last_7_days(request):
    user = request.user
    seven_days_ago = timezone.now() - timedelta(days = 7)
    rent_history = Rent.objects.filter(user = user, rent_date__gte = seven_days_ago)
    serializer = MyRentSerializer(rent_history, many = True)
    return serializer.data


class MyPageView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user) 

        myuser_serializer = MyUserSerializer(user)
        myprofile_serializer = MyProfileSerializer(profile)
        history = rent_history_last_7_days(request)
        print(history)
        mypage_data = {
            'user': {
                'username': myuser_serializer.data['username'],
                'studentID': myprofile_serializer.data['studentID'],
                'phoneNumber': myprofile_serializer.data['phoneNumber'],
                'email': myuser_serializer.data['email'],
            },
            'history': history,
        }
        return Response(mypage_data, status = status.HTTP_200_OK)