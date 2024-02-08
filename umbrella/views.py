#umbrella/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Umbrella
from .serializers import UmbrellaSerializer, UserSerializer


class UmbrellaViewSet(viewsets.ModelViewSet):
    queryset = Umbrella.objects.all()
    serializer_class = UmbrellaSerializer


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

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    else:
        return Response({'error': 'User has an umbrella already.'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def return_umbrella(request):
    user = request.user
    profile = user.profile

    if profile.umbrella:
        umbrella = profile.umbrella
        umbrella.is_available = True
        umbrella.save()

        profile.umbrella = None
        profile.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    else:
        return Response({'error': 'User does not have an umbrella to return.'}, status = status.HTTP_400_BAD_REQUEST)
