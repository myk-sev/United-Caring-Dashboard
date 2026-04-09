from django.urls import path
from . import views

urlpatterns = [
path('', views.shelters_home, name='shelters'),
]