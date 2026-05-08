"""
WhiteFlag Model

This model represents shelter occupancy tracking data within the UCS system.

It stores demographic counts (men, women, children, non-binary individuals)
and automatically calculates the total number of individuals.

The model is used to:
- Track shelter occupancy submissions
- Maintain historical records of entries
- Support reporting and analytics features in the dashboard
"""

from django.db import models

# Create your models here.



class WhiteFlag(models.Model):
    """
    Database model for storing WhiteFlag shelter capacity records.
    Each record represents a snapshot of shelter population at a given time.
    """
    
    record_number = models.AutoField(primary_key=True)

    # Demographic breakdown of shelter population
    men           = models.PositiveIntegerField(default=0)
    women         = models.PositiveIntegerField(default=0)
    children      = models.PositiveIntegerField(default=0)
    non_binary    = models.PositiveIntegerField(default=0)

    # Automatically calculated total population
    total         = models.PositiveIntegerField(default=0)

    # Timestamp of when the record was created
    submitted_at  = models.DateTimeField(auto_now_add=True)


    class Meta:
        # Defines app association and default ordering
        app_label = 'whiteflag'
        ordering  = ['-submitted_at']

    def save(self, *args, **kwargs):
        """
        Override save method to ensure total is always accurate.

        The total is automatically calculated from all demographic fields
        before saving to maintain data consistency and avoid manual errors.
        """

        self.total = self.men + self.women + self.children + self.non_binary
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the record for admin/debugging.

        Displays record number and submission timestamp.
        """
        
        return f"Record #{self.record_number} — {self.submitted_at:%Y-%m-%d %H:%M}"
