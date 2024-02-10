#umbrella/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Umbrella, Rent
from .serializers import UmbrellaSerializer, RentSerializer
from datetime import *
from django.utils import timezone
from django.db.models import Count
import json


@api_view(['GET'])
def get_available_umbrellas(request):
    location_counts = Umbrella.objects.filter(is_available = True).values('location').annotate(num_umbrellas = Count('id'))

    result_list = []
    for location_count in location_counts:
        location_id = Umbrella().get_location_id(location_count['location'])
        result_list.append({'location_id': location_id, 'num_umbrellas': location_count['num_umbrellas']})
        result_list = sorted(result_list, key = lambda x: x["location_id"])
    return Response(result_list, status = status.HTTP_200_OK)


@api_view(['POST'])
def lend_umbrella(request, umbrella_number):
    user = request.user

    try:
        umbrella = Umbrella.objects.get(number = umbrella_number, is_available = True)
    except Umbrella.DoesNotExist:
        return Response({'error': f'Umbrella {umbrella_number} is not available for lending.'}, status = status.HTTP_400_BAD_REQUEST)

    profile = user.profile
    if profile.umbrella is None:
        umbrella.is_available = False
        umbrella.save()

        profile.umbrella = umbrella
        profile.save()

        rent_serializer = RentSerializer(data = {'user': user.id, 'umbrella': umbrella.id})
        if rent_serializer.is_valid():
            rent_serializer.save()
            return Response({'message': 'Umbrella lent successfully.'}, status = status.HTTP_200_OK)
    else:
        return Response({'error': 'User has an umbrella already.'}, status = status.HTTP_400_BAD_REQUEST)


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
        return Response({'message': 'Umbrella returned successfully.'}, status = status.HTTP_200_OK)
    else:
        return Response({'error': 'User does not have an umbrella to return.'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_days_remaining(request):
    user = request.user
    rent = Rent.objects.filter(user = user, return_date = None).first()

    if rent and rent.return_due_date:
        is_overdue = datetime.now() > rent.return_due_date
        overdue_days = max(0, (datetime.now() - rent.return_due_date).days) if is_overdue else 0

        response_data = {
            'is_overdue': is_overdue,
            'overdue_days': overdue_days,
            'days_remaining': max(0, (rent.return_due_date - datetime.now()).days)
        }
        return Response(response_data, status = status.HTTP_200_OK)
    else:
        return Response({'is_overdue': 'False', 'overdue_days': 0,'days_remaining': 0 }, status = status.HTTP_200_OK)


@api_view(['GET'])
def rent_history_last_7_days(request):
    user = request.user
    seven_days_ago = timezone.now() - timedelta(days = 7)
    rent_history = Rent.objects.filter(user = user, rent_date__gte = seven_days_ago)
    serializer = RentSerializer(rent_history, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
