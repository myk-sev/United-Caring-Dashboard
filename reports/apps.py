"""
Reports App Configuration

This module defines the configuration for the 'reports' Django application
within the UCS system.

It registers the reports app with Django so it can be included in the
project’s installed applications and properly initialized.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuration class for the reports application.

    This class is used by Django to initialize and manage the reports
    app within the overall project structure.
    """
    
    # Name of the Django application
    name = 'reports'
