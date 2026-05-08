"""
Accounts URL Configuration

This module defines URL routes for user authentication in the UCS system.

It connects URLs to authentication-related views such as:
- Login page
- Logout action

These routes control user access to the application.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Default landing page (login screen)
    path('', views.login_view, name='login'),   # THIS is your homepage now
    
    # Explicit login route
    path('login/', views.login_view, name='login'),
    
    # Logout route
    path('logout/', views.logout_view, name='logout'),
]