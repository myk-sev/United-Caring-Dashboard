"""
Shelters Admin Configuration

This module registers Django models with the admin site
for the shelters application in the UCS dashboard.

It allows administrative users to view and manage Shelter
data through Django’s built-in admin interface.
"""

from django.contrib import admin
from .models import ShelterInputModel

# Register the Shelter model in Django admin interface
# This enables CRUD operations for shelter records via admin panel
admin.site.register(ShelterInputModel)
