from django import forms
from django.db import models


class ShelterInputModel(models.Model):
    date = models.DateField(auto_now_add=True)
    shelter = models.CharField(max_length=100)
    regular = models.IntegerField()
    respite = models.IntegerField()
    guests = models.IntegerField()
    hospital = models.IntegerField()
    jail = models.IntegerField()
    no_show = models.IntegerField()
    barred = models.IntegerField()
    hold = models.IntegerField()

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    total_beds = models.IntegerField()
    respite_beds = models.IntegerField()

    def __str__(self):
        return self.name
