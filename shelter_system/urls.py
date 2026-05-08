"""
Project URL Configuration

This module defines the root URL routing for the UCS Shelter System project.

It connects different Django apps to specific URL paths, allowing users
to navigate between different system modules such as:
- Authentication (accounts)
- Dashboard
- Reports
- Shelters
- White Flag tracking
- Admin panel
- Main screen

This acts as the central routing hub for the entire application.
"""

from django.contrib import admin
from django.urls import path, include

import mainscreen.views

urlpatterns = [
    # Main landing page (home screen)
    path('', include('mainscreen.urls')),

    # Django admin panel
    path('admin/', admin.site.urls),

    # User authentication system (login, signup, etc.)
    path('', include('accounts.urls')),

    # Dashboard module
    path('dashboard/', include('dashboard.urls')),

    # Reports module (CSV export/import, filtering, analytics)
    path('reports/', include('reports.urls')),

    # Shelters management module (intake and tracking)
    path('shelters/', include('shelters.urls')),

    # White Flag tracking module
    path('white-flag/', include('whiteflag.urls')),

    # Admin panel custom interface
    path('', include('admin_panel.urls')),
]