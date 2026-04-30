from django.urls import path
from . import views

urlpatterns = [
    path('',          views.white_flag,      name='white_flag'),
    path('<int:pk>/', views.white_flag_edit, name='white_flag_edit'),
]