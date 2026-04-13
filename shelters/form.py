from django import forms
from shelters.models import ShelterInputModel

class ShelterInputForm(forms.ModelForm):
    class Meta:
        model = ShelterInputModel
        fields = ["shelter",
                "regular_occupied",
                "regular_open",
                "guests_on_pass",
                "hospital",
                "jail",
                "nc_ns",
                "barred",
                "hold",
                "respite_occupied",
                "respite_open"
                ]