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

        myuser = MyUserSerializer(user)
        myprofile = MyProfileSerializer(profile)
        history = rent_history_last_7_days(request)
        if not history:
            history = '아직 내역이 없어요'
        mypage_data = {
            'status': status.HTTP_200_OK,
            'message': '응답 성공',
            'data': {
                'user': {
                    'id': myuser.data['id'],
                    'username': myuser.data['username'],
                    'studentID': myprofile.data['studentID'],
                    'phoneNumber': myprofile.data['phoneNumber'],
                    'email': myuser.data['email'],
                },
                'history': history,
            }
        }
        return Response(mypage_data, status = mypage_data['status'])