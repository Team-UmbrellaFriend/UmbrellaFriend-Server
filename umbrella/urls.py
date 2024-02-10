#umbrella/urls.pu
from django.urls import path
from .views import *


urlpatterns = [
    path('available/', get_available_umbrellas),
    path('<int:umbrella_number>/lend/', lend_umbrella),
    path('return/', return_umbrella),
    path('history/', rent_history_last_7_days),
]
