#umbrella/urls.pu
from django.urls import path
from .views import *


urlpatterns = [
    path('<int:umbrella_number>/lend/', lend_umbrella),
    path('return/', return_umbrella),
]
