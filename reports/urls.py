Reports URL Configuration

This module defines URL routes for the reports system in the UCS application.

It connects reporting-related endpoints to their corresponding views,
including:
- Reports dashboard (filtering view)
- CSV export functionality
- CSV import functionality

These routes enable data analysis and data transfer features.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Reports dashboard with filtering options
    path('', views.reports_home, name='reports'),
    
    # Export filtered data to CSV file
    path('export/', views.export_all_data, name='export'),
    
    # Import CSV data into the system
    path('import/', views.import_all_data, name='import'),
]
