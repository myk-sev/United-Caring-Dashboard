"""
Reports Admin Configuration

This module customizes the Django admin interface for the reports system.

It defines how ShiftReport data is displayed, filtered, and searched
within the Django admin panel to improve usability for administrators.
"""

from django.contrib import admin
from .models import ShiftReport

@admin.register(ShiftReport)
class ShiftReportAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for ShiftReport model.

    Enhances admin usability by:
    - Displaying key fields in list view
    - Enabling filtering by shelter and date
    - Allowing search by report number
    """

    # Columns shown in admin list view
    list_display = ('report_number', 'shelter', 'shift', 'beds_used', 'beds_available', 'date')
    
    # Sidebar filters for quick data sorting
    list_filter = ('shelter', 'date')
    
    # Search functionality in admin panel
    search_fields = ('report_number',)
