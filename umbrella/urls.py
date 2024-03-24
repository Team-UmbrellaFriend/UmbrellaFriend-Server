#umbrella/urls.pu
from django.urls import path
from .views import *


urlpatterns = [
    path('available/', get_available_umbrellas),
    path('<int:umbrella_number>/lend/', lend_umbrella),
    path('<int:umbrella_number>/check/', check_umbrella),
    path('return/', return_umbrella),
    path('extend/', extend_return_due_date),
]
