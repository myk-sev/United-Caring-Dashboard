"""
Admin Panel App Configuration

This module defines the configuration for the 'admin_panel' Django application
within the UCS system.

It registers the app with Django and sets default configuration options
used during database model creation and application initialization.
"""

from django.apps import AppConfig


class AdminPanelConfig(AppConfig):

    # Default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the Django application
    name = 'admin_panel'
