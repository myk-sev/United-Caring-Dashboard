from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),   # THIS is your homepage now
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]