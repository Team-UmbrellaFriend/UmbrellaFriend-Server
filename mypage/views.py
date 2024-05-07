from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from umbrella.models import Rent, Umbrella
from users.models import Profile
from .models import UmbrellaReport
from .serializers import *
from datetime import *
from django.utils import timezone
from rest_framework.decorators import api_view


def rent_history_last_7_days(request):
    user = request.user
    seven_days_ago = timezone.now() - timedelta(days = 7)
    rent_history = Rent.objects.filter(user = user, rent_date__gte = seven_days_ago).order_by('-rent_date')
    serializer = MyRentSerializer(rent_history, many = True)
    return serializer.data


class MyPageView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user) 

        myuser = MyUserSerializer(user)
        myprofile = MyProfileSerializer(profile)
        history = rent_history_last_7_days(request)

        formatted_phone_number = self.format_phone_number(myprofile.data['phoneNumber'])

        mypage_data = {
            'status': status.HTTP_200_OK,
            'message': '응답 성공',
            'data': {
                'user': {
                    'id': myuser.data['id'],
                    'username': myuser.data['username'],
                    'studentID': myprofile.data['studentID'],
                    'phoneNumber': formatted_phone_number,
                    'email': myuser.data['email'],
                },
                'history': history,
            }
        }
        return Response(mypage_data, status = mypage_data['status'])


    def format_phone_number(self, raw_phone_number):
        formatted_phone_number = f'{raw_phone_number[:3]}-{raw_phone_number[3:7]}-{raw_phone_number[7:]}'
        return formatted_phone_number


@api_view(['POST'])
def report_umbrella(request):
    user = request.user

    umbrella_number = request.data.get('umbrella_number')
    report_reason = request.data.get('report_reason')
    description = request.data.get('description')

    valid_choices = [choice[0] for choice in UmbrellaReport.REPORT_CHOICES] # choice[0] 각 튜플의 첫 번째 요소
    if report_reason not in valid_choices:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '유효하지 않은 신고 사유입니다.', 'data': ''}, status = status.HTTP_400_BAD_REQUEST)

    if report_reason == '기타':
        if not description:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '기타 사유를 입력해주세요.', 'data': ''}, status = status.HTTP_400_BAD_REQUEST)

    try:
        umbrella = Umbrella.objects.get(number = umbrella_number)
    except Umbrella.DoesNotExist:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f'우산[{umbrella_number}]을 찾을 수 없습니다.', 'data': ''}, status = status.HTTP_400_BAD_REQUEST)

    report_data = {'user': user.id, 'umbrella': umbrella.id, 'report_reason': report_reason, 'description': description}
    report_serializer = ReportSerializer(data = report_data)
    if report_serializer.is_valid():
        report_serializer.save()

        umbrella.has_issue = True
        umbrella.save()

        return Response({'status': status.HTTP_201_CREATED, 'message': '우산 신고가 성공적으로 제출되었습니다.', 'data': ''}, status = status.HTTP_201_CREATED)
    else:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '우산 신고 실패', 'data': ''}, status = status.HTTP_400_BAD_REQUEST)