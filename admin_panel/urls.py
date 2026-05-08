"""
Admin Panel URL Configuration

This module defines URL routes for the UCS administrative panel.

It connects URL paths to their corresponding view functions,
allowing navigation between:
- Admin login
- Admin dashboard page one (analytics)
- Admin dashboard page two (record management)
- Admin logout functionality
"""

from django.urls import path
from . import views

urlpatterns = [
    # Admin login page
    path('admin-panel/',          views.admin_login,    name='admin_login'),

    # Admin dashboard - analytics overview
    path('admin-panel/page-one/', views.admin_page_one, name='admin_page_one'),
    
    # Admin dashboard - record management and editing
    path('admin-panel/page-two/', views.admin_page_two, name='admin_page_two'),
    
    # Admin logout endpoint
    path('admin-panel/logout/',   views.admin_logout,   name='admin_logout'),
]