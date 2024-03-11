#home/views.py
from rest_framework.views import APIView
from umbrella.models import Rent
from rest_framework.response import Response
from rest_framework import status
from datetime import *
from weather.views import get_rain_percent
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_days_remaining(request):
    user = request.user
    rent = Rent.objects.filter(user = user, return_date = None).first()
    overdue_rent = Rent.objects.filter(user = user, return_date__isnull = False, is_disabled = True).first()
    if overdue_rent:
        overdue_period = int(overdue_rent.rental_period.split('일간')[0])


    if rent and rent.return_due_date:
        is_overdue = rent.is_overdue()
        overdue_days = max(0, (datetime.now() - rent.return_due_date).days + 1) if is_overdue else 0

        response_data = {
            'is_overdue': is_overdue,
            'overdue_days': overdue_days,
            'days_remaining': max(0, (rent.return_due_date - datetime.now()).days)
        }
        return response_data
    elif overdue_rent and overdue_period > 3:
        # 대여 중이 아니지만 이전에 연체된 기록이 있는 경우 해당 정보를 반환

        current_date = timezone.now()
        return_date = overdue_rent.return_date

        initial_overdue_days = overdue_period - 3
        overdue_days = initial_overdue_days - (current_date - return_date).days

        logger.info("initial_overdue_days: %s", initial_overdue_days)
        logger.info("difference: %s", current_date - return_date)
        logger.info('-------')
        logger.info("User: %s", overdue_rent.user)
        logger.info("Umbrella: %s", overdue_rent.umbrella)
        logger.info("Rent Date: %s", overdue_rent.rent_date)
        logger.info("Return Date: %s", overdue_rent.return_date)
        logger.info("Return Due Date: %s", overdue_rent.return_due_date)
        logger.info("Rental Period: %s", overdue_rent.rental_period)

        if overdue_days < 0:
            overdue_rent.is_disabled = False
            overdue_rent.flag_save()
            logger.info("is_disabled: %s", overdue_rent.is_disabled)
            return {'is_overdue': False, 'overdue_days': -1,'days_remaining': -1}
        
        response_data = {
            'is_overdue': True,
            'overdue_days': overdue_days,
            'days_remaining': 0
        }
        return response_data
    else:
        return {'is_overdue': False, 'overdue_days': -1,'days_remaining': -1}


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        days_remaining = get_days_remaining(request)
        weather_data = get_rain_percent(request)

        percent_value = int(weather_data['percent']) if isinstance(weather_data['percent'], str) and weather_data['percent'].isdigit() else -1
        weather_message = ''
        if days_remaining.get('is_overdue') == False and days_remaining.get('days_remaining') != -1:
            weather_message = f'우산 반납일까지 { days_remaining["days_remaining"] }일 남았습니다!'
        elif days_remaining.get('is_overdue') == True:
            weather_message = f'연체로 인해 {abs(days_remaining["overdue_days"])}일간 대여가 불가능합니다.'
        elif 0 <= percent_value <= 20:
            weather_message = '오늘은 비가 올 확률이 적네요!'
        elif 20 < percent_value <= 60:
            weather_message = '비가 올 수도 있어요!'
        elif percent_value > 60:
            weather_message = '오늘은 비가 올 확률이 높네요!'

        home_data = {
            'status': status.HTTP_200_OK,
            'message': '응답 성공',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                },
                'weather': {
                    'weather': weather_data,  
                    'message': weather_message,
                },
                'd-day': days_remaining,
            }
        }
        if not weather_data['date']:
            home_data['status'] = status.HTTP_400_BAD_REQUEST
            home_data['message'] = '응답 실패'
        return Response(home_data, status = home_data['status'])