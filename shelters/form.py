from django import forms
from shelters.models import ShelterInputModel
from .models import WhiteFlag

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
        
class WhiteFlagForm(forms.ModelForm):
    class Meta:
        model  = WhiteFlag
        fields = ['men', 'women', 'children', 'non_binary']
        labels = {
            'men'       : 'Number of Men',
            'women'     : 'Number of Women',
            'children'  : 'Number of Children',
            'non_binary': 'Number of Non-Binary',
        }
        widgets = {
            'men'       : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'women'     : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'children'  : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'non_binary': forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
        }