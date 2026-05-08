"""
Admin Panel Models

This module defines database models used for administrative configuration
within the UCS system.

It currently contains settings related to admin authentication.
"""

from django.db import models

# Create your models here.
class AdminSettings(models.Model):
    """
    Stores system-wide administrative configuration values.

    Currently used to store the admin panel password.

    NOTE:
    This implementation is intended for development/testing purposes.
    In production, this should be replaced with Django's built-in
    authentication system and hashed passwords for security.
    """

    # Admin login password (temporary implementation)
    admin_password = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Admin Settings"

    def __str__(self):
        return "Admin Settings"