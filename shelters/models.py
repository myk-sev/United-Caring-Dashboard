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
class WhiteFlag(models.Model):
    record_number = models.AutoField(primary_key=True)
    men           = models.PositiveIntegerField(default=0)
    women         = models.PositiveIntegerField(default=0)
    children      = models.PositiveIntegerField(default=0)
    non_binary    = models.PositiveIntegerField(default=0)
    total         = models.PositiveIntegerField(default=0)
    submitted_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'United-Caring-Dashboard'
        ordering  = ['-submitted_at']

    def save(self, *args, **kwargs):
        self.total = self.men + self.women + self.children + self.non_binary
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Record #{self.record_number} — {self.submitted_at:%Y-%m-%d %H:%M}"   