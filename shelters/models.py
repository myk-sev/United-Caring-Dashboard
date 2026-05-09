"""
Shelters Models

This module defines the database structure for the shelters system
within the UCS dashboard.

It stores shelter intake data, including occupancy tracking and
bed capacity information for different shelter types.
"""

from django import forms
from django.db import models


class ShelterInputModel(models.Model):
    """
    Represents a daily shelter intake record.

    This model tracks how many individuals are assigned to
    different categories within a shelter system, including:
    - Regular admissions
    - Respite care
    - Guests
    - Hospital transfers
    - Jail transfers
    - No-shows
    - Barred individuals
    - Holds

    Each record is timestamped automatically when created.
    """

    # Date the record was created (auto-generated)
    date = models.DateField(auto_now_add=True)

    # Shelter type associated with this record
    shelter = models.CharField(max_length=100)

    # Breakdown of shelter occupancy categories
    regular = models.IntegerField()
    respite = models.IntegerField()
    guests = models.IntegerField()
    hospital = models.IntegerField()
    jail = models.IntegerField()
    no_show = models.IntegerField()
    barred = models.IntegerField()
    hold = models.IntegerField()

class Shelter(models.Model):
    """
    Represents a shelter location and its capacity configuration.

    Stores basic shelter information including:
    - Shelter name
    - Total bed capacity
    - Respite bed capacity
    """

    name = models.CharField(max_length=100)
    total_beds = models.IntegerField()
    respite_beds = models.IntegerField()

    def __str__(self):
        """
        Returns a readable name for the shelter object
        (used in admin panel and debugging).
        """
        
        return self.name