from django.contrib import admin
from .models import ShiftReport

@admin.register(ShiftReport)
class ShiftReportAdmin(admin.ModelAdmin):
    list_display = ('report_number', 'shelter', 'shift', 'beds_used', 'beds_available', 'date')
    list_filter = ('shelter', 'date')
    search_fields = ('report_number',)