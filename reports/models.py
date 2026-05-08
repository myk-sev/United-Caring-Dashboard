"""
Reports Models

This module defines database models used for reporting functionality
within the UCS system.

It includes the ShiftReport model, which stores operational shift data
related to shelter capacity usage and availability.
"""

from django.db import models
from shelters.models import Shelter, ShelterInputModel
class ShiftReport(models.Model):
    """
    Represents a shift-based operational report for a shelter.

    This model tracks:
    - Shelter name
    - Shift type (e.g., morning, evening, night)
    - Beds used and available
    - Auto-generated timestamp
    - Custom report identifier
    """

    # Name of the shelter associated with the shift
    shelter = models.CharField(max_length=100)
    
    # Type of shift (morning, evening, night, etc.)
    shift = models.CharField(max_length=50)
    
    # Number of beds currently used during the shift
    beds_used = models.IntegerField()
    
    # Number of beds available during the shift
    beds_available = models.IntegerField()
    
    # Timestamp when the report was created
    date = models.DateTimeField(auto_now_add=True)
    
    # Unique identifier for the report (custom tracking field)
    report_number = models.CharField(max_length=50, default='')#This adds the report number field to the ShiftReport model, 
        #ensuring that each report has a unique identifier.

    def __str__(self):
        """
        String representation of the ShiftReport model.

        Returns a readable format combining shelter and shift type.
        """
        
        return f"{self.shelter} - {self.shift}"
