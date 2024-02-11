#home/views.py
from rest_framework.views import APIView
from umbrella.models import Rent
from rest_framework.response import Response
from rest_framework import status
from datetime import *
from weather.views import get_rain_percent


def get_days_remaining(request):
    user = request.user
    rent = Rent.objects.filter(user = user, return_date = None).first()

    if rent and rent.return_due_date:
        is_overdue = datetime.now() > rent.return_due_date
        overdue_days = max(0, (datetime.now() - rent.return_due_date).days + 1) if is_overdue else 0

        response_data = {
            'is_overdue': is_overdue,
            'overdue_days': overdue_days,
            'days_remaining': max(0, (rent.return_due_date - datetime.now()).days + 1)
        }
        return response_data
    else:
        return {'is_overdue': 'False', 'overdue_days': 0,'days_remaining': 0}


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        days_remaining = get_days_remaining(request)
        weather_data = get_rain_percent(request)
        home_data = {
            'username': user.username,
            'weather': weather_data,
            'd-day': days_remaining,
        }
        if weather_data['date']:
            return Response(home_data, status = status.HTTP_200_OK)
        else:
            return Response(home_data, status = status.HTTP_400_BAD_REQUEST)