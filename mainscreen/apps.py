"""
Mainscreen App Configuration

This module defines the configuration for the 'mainscreen' Django application
within the UCS system.

It registers the app so Django can recognize and include it in the
project’s installed applications list.
"""

from django.apps import AppConfig


class MainscreenConfig(AppConfig):
    """
    Configuration class for the mainscreen application.

    This class is used by Django to initialize and manage the mainscreen
    app within the overall project structure.
    """
    
    name = 'mainscreen'
