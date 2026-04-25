from django.urls import include, path
from . import views

urlpatterns = [
path('', views.shelters_home, name='shelters'),
#path('', include('mainscreen.urls')),

]