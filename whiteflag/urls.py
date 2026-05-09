"""
WhiteFlag URL Configuration

This module defines URL routes for the WhiteFlag feature
within the UCS dashboard system.

It connects URL patterns to their corresponding view functions:
- Creating a new WhiteFlag record
- Editing an existing WhiteFlag record

These routes control navigation for WhiteFlag-related pages.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Route for creating a new WhiteFlag record (main entry page)
    path('',          views.white_flag,      name='white_flag'),

    # Route for editing an existing WhiteFlag record by primary key (pk
    path('<int:pk>/', views.white_flag_edit, name='white_flag_edit'),
]