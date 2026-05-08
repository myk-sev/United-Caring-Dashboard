"""
Forms Module

This module defines form structures used in the UCS dashboard system.

It includes:
- ShelterInputForm: used for shelter intake data entry
- WhiteFlagForm: used for tracking WhiteFlag shelter capacity data

These forms handle:
- Input validation
- Data formatting
- User interface customization (labels, widgets)
"""

from django import forms
from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag

class ShelterInputForm(forms.ModelForm):
    """
    Form used to collect shelter intake data.

    This form maps directly to the ShelterInputModel and is used
    to record daily shelter statistics such as regular intake,
    respite care, hospital transfers, and other categories.
    """
    
    class Meta:
        model = ShelterInputModel

        # Fields included in the shelter intake form
        fields = [ "shelter",
                   "regular",
                   "respite",
                   "guests",
                   "hospital",
                   "jail",
                   "no_show",
                   "barred",
                   "hold" ]
        
class WhiteFlagForm(forms.ModelForm):
    """
    Form used to collect WhiteFlag shelter capacity data.

    This form handles demographic input including:
    - Men
    - Women
    - Children
    - Non-binary individuals

    It also includes UI customization for better user experience.
    """
    
    class Meta:
        model  = WhiteFlag

        # Fields included in the WhiteFlag form
        fields = ['men', 'women', 'children', 'non_binary']

        # Human-readable labels for UI display
        labels = {
            'men'       : 'Number of Men',
            'women'     : 'Number of Women',
            'children'  : 'Number of Children',
            'non_binary': 'Number of Non-Binary',
        }

        # UI widgets with validation and styling
        widgets = {
            'men'       : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'women'     : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'children'  : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'non_binary': forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
        }