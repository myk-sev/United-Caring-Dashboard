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
    Legacy table retained for migration compatibility.

    Admin-panel authentication now reads ADMIN_PANEL_PASSWORD directly
    from the environment.
    """

    # Legacy field retained for migration compatibility.
    admin_password = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Admin Settings"

    def __str__(self):
        return "Admin Settings"
