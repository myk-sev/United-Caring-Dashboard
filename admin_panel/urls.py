from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/',          views.admin_login,    name='admin_login'),

    path('admin-panel/page-one/', views.admin_page_one, name='admin_page_one'),
    path('admin-panel/page-two/', views.admin_page_two, name='admin_page_two'),
    path('admin-panel/logout/',   views.admin_logout,   name='admin_logout'),
]