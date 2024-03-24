#umbrella/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Umbrella, Rent
from .serializers import RentSerializer
from datetime import *
from django.utils import timezone
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
import logging


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_available_umbrellas(request):
    location_counts = Umbrella.objects.filter(is_available = True).values('location').annotate(num_umbrellas = Count('id'))
    location_mapping = {
        1: '명신관',
        2: '순헌관',
        3: '학생회관',
        4: '도서관',
        5: '음대',
        6: '백주년기념관',
    }

    result_list = []
    for location_id in range(1, 7):
        matching_location = next((lc for lc in location_counts if Umbrella().get_location_id(lc['location']) == location_id), None)
        location_name = location_mapping.get(location_id, '장소 없음')

        if matching_location:
            result_list.append({'location_id': location_id, 'location_name': location_name, 'num_umbrellas': matching_location['num_umbrellas']})
        else:
            result_list.append({'location_id': location_id, 'location_name': location_name, 'num_umbrellas': 0})

        available_data = {
            'status': status.HTTP_200_OK,
            'message': '응답 성공',
            'data': result_list
        }
    return Response(available_data, status = available_data['status'])


@api_view(['GET'])
def check_umbrella(request, umbrella_number):
    user = request.user
    profile = user.profile
    now = timezone.now()
    three_days_later = now + timezone.timedelta(days = 3)

    check_data = {
        'status': status.HTTP_200_OK,
        'message': '응답 성공',
        'data': {
            'umbrella_num': umbrella_number,
            'username': user.username,
            'studentID': profile.studentID,
            'date': now.strftime("%Y/%m/%d") + "~" + three_days_later.strftime("%Y/%m/%d")
        }
    }
    return Response(check_data, status = check_data['status'])


@api_view(['POST'])
def lend_umbrella(request, umbrella_number):
    user = request.user

    try:
        umbrella = Umbrella.objects.get(number = umbrella_number, is_available = True)
    except Umbrella.DoesNotExist:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f'우산 {umbrella_number}는 대여할 수 없습니다', 'data': ''}, status = status.HTTP_400_BAD_REQUEST)

    lend_data = {
        'status': status.HTTP_400_BAD_REQUEST,
        'message': '대여 중인 우산을 반납하고 시도해주세요',
        'data': ''
    }

    profile = user.profile
    if profile.umbrella is None:
        umbrella.is_available = False
        umbrella.save()

        profile.umbrella = umbrella
        profile.save()

        rent_serializer = RentSerializer(data = {'user': user.id, 'umbrella': umbrella.id})
        if rent_serializer.is_valid():
            rent_serializer.save()
            lend_data['status'] = status.HTTP_200_OK
            lend_data['message'] = '우산을 대여했습니다'
    return Response(lend_data, status = lend_data['status'])


@api_view(['POST'])
def return_umbrella(request):
    user = request.user
    profile = user.profile
    data = request.data
    location = data.get('location')

    return_data = {
        'status': status.HTTP_200_OK,
        'message': '우산을 반납했습니다',
        'data': ''
    }

    if profile.umbrella:
        umbrella = profile.umbrella
        if umbrella.get_location_id(location) not in umbrella.place.values():
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '유효하지 않은 장소입니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)
        return_image = data.get('return_image')
        if not return_image :
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '인증 사진이 없습니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)
        
        rent = None
        try:
            rent = Rent.objects.get(umbrella=umbrella.number, user=user.id, return_date=None)
        except ObjectDoesNotExist:
            logger.error("대여 중인 우산 정보를 찾을 수 없습니다. Umbrella: %s, User: %s", umbrella.number, user.id)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '대여 중인 우산 정보를 찾을 수 없습니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)
        except Rent.MultipleObjectsReturned:
            logger.error("대여 중인 우산 정보가 여러 개입니다. Umbrella: %s, User: %s", umbrella.number, user.id)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '대여 중인 우산 정보가 여러 개입니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)
    
        if rent:
            umbrella.is_available = True
            umbrella.location = location
            umbrella.save()

            profile.umbrella = None
            profile.save()

            rent.return_date = timezone.now()
            rent.image = return_image
            rent.save()
    else:
        return_data['status'] = status.HTTP_400_BAD_REQUEST
        return_data['message'] = '반납할 우산이 없습니다'
    return Response(return_data, status = return_data['status'])


@api_view(['GET'])
def extend_return_due_date(request):
    user = request.user

    try:
        rent = Rent.objects.get(user = user, return_date__isnull = True)
    except Rent.DoesNotExist:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '대여 중인 우산 정보를 찾을 수 없습니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)

    if rent.is_overdue():
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': '연체된 사용자는 연장할 수 없습니다', 'data':''}, status = status.HTTP_400_BAD_REQUEST)

    if rent.extension_count == 0:
        rent.extension_count += 1
        rent.return_due_date += timezone.timedelta(days=3)
        rent.save()

    return Response({'status': status.HTTP_200_OK, 'message': '대여 연장 성공', 'data': {'extension_count' : rent.extension_count}}, status = status.HTTP_200_OK)