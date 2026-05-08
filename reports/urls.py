from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_home, name='reports'),
    path('export/', views.export_all_data, name='export'),
    path('import/', views.import_all_data, name='import'),
]