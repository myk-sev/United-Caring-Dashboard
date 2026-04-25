# mainscreen/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainscreen, name='mainscreen'),
]