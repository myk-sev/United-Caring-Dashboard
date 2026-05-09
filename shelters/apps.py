"""
Shelters App Configuration

This module defines the configuration for the 'shelters' Django application
within the UCS dashboard system.

It registers the app with Django and allows it to be included in the
project’s installed applications.
"""

from django.apps import AppConfig


class SheltersConfig(AppConfig):
    """
    Configuration class for the shelters application.

    This class is used by Django to recognize and configure the
    shelters app within the overall project structure.
    """

    # Name of the Django application
    name = 'shelters'
