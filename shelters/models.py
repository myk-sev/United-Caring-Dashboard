from django import forms
from django.db import models


class ShelterInputModel(models.Model):
    shelter = models.CharField(max_length=100)
    regular_occupied = models.IntegerField()
    regular_open = models.IntegerField()
    guests_on_pass = models.IntegerField()
    hospital = models.IntegerField()
    jail = models.IntegerField()
    nc_ns = models.IntegerField()
    barred = models.IntegerField()
    hold = models.IntegerField()
    respite_occupied = models.IntegerField()
    respite_open = models.IntegerField()

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    total_beds = models.IntegerField()
    respite_beds = models.IntegerField()

    def __str__(self):
        return self.name