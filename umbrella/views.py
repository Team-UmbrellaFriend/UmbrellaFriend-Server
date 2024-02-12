#umbrella/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Umbrella, Rent
from .serializers import RentSerializer
from datetime import *
from django.utils import timezone
from django.db.models import Count
import json


@api_view(['GET'])
def get_available_umbrellas(request):
    location_counts = Umbrella.objects.filter(is_available = True).values('location').annotate(num_umbrellas = Count('id'))

    result_list = []
    for location_id in range(1, 7):
        matching_location = next((lc for lc in location_counts if Umbrella().get_location_id(lc['location']) == location_id), None)

        if matching_location:
            result_list.append({'location_id': location_id, 'num_umbrellas': matching_location['num_umbrellas']})
        else:
            result_list.append({'location_id': location_id, 'num_umbrellas': 0})

    return Response(result_list, status = status.HTTP_200_OK)


@api_view(['POST'])
def lend_umbrella(request, umbrella_number):
    user = request.user

    try:
        umbrella = Umbrella.objects.get(number = umbrella_number, is_available = True)
    except Umbrella.DoesNotExist:
        return Response({'error': f'우산 {umbrella_number}는 대여할 수 없습니다'}, status = status.HTTP_400_BAD_REQUEST)

    profile = user.profile
    if profile.umbrella is None:
        umbrella.is_available = False
        umbrella.save()

        profile.umbrella = umbrella
        profile.save()

        rent_serializer = RentSerializer(data = {'user': user.id, 'umbrella': umbrella.id})
        if rent_serializer.is_valid():
            rent_serializer.save()
            return Response({'message': '우산을 대여했습니다'}, status = status.HTTP_200_OK)
    else:
        return Response({'error': '대여 중인 우산을 반납하고 시도해주세요'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_umbrella(request, umbrella_number):
    user = request.user
    profile = user.profile
    now = timezone.now()
    three_days_later = now + timezone.timedelta(days = 3)
    check_data = {
        'umbrella_num': umbrella_number,
        'username': user.username,
        'studentID': profile.studentID,
        'date': now.strftime("%Y/%m/%d") + "~" + three_days_later.strftime("%Y/%m/%d")
    }
    return Response(check_data, status = status.HTTP_200_OK)


@api_view(['POST'])
def return_umbrella(request):
    user = request.user
    profile = user.profile
    data = json.loads(request.body)
    location = data.get('location')
    if profile.umbrella:
        umbrella = profile.umbrella
        umbrella.is_available = True
        umbrella.location = location
        umbrella.save()

        profile.umbrella = None
        profile.save()

        rent = Rent.objects.get(umbrella = umbrella.number, user = user.id, return_date = None)
        rent.return_date = timezone.now()
        rent.save()
        return Response({'message': '우산을 반납했습니다'}, status = status.HTTP_200_OK)
    else:
        return Response({'error': '반납할 우산이 없습니다'}, status = status.HTTP_400_BAD_REQUEST)