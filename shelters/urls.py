"""
Shelters URL Configuration

This module defines URL routes for the shelters feature
within the UCS dashboard system.

It connects URL patterns to view functions responsible for:
- Displaying the shelters intake page
- Handling shelter form submissions and data processing
"""

from django.urls import include, path
from . import views

urlpatterns = [

    # Main shelters intake page (handles both display and form submission)
    path('', views.shelters_home, name='shelters')
]