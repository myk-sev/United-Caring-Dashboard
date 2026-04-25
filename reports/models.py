from django.db import models
from shelters.models import Shelter

class ShiftReport(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    shift = models.CharField(max_length=50)
    beds_used = models.IntegerField()
    beds_available = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    report_number = models.CharField(max_length=50, default='')#This adds the report number field to the ShiftReport model, 
        #ensuring that each report has a unique identifier.

    def __str__(self):
        return f"{self.shelter} - {self.shift}"