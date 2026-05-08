"""
WhiteFlag Form

This form is used to collect shelter population data for the WhiteFlag system.

It handles input validation and user-friendly display of demographic fields,
including men, women, children, and non-binary individuals.

The form ensures:
- Clean numeric input
- Minimum value validation (no negative numbers)
- Consistent UI formatting across all fields
"""

from django import forms
from .models import WhiteFlag


class WhiteFlagForm(forms.ModelForm):
    """
    ModelForm for creating and updating WhiteFlag records.

    Provides structured input fields for shelter population tracking
    with customized labels and input widgets for better usability.
    """

    class Meta:
        model  = WhiteFlag

        # Fields included in the form (excludes auto-calculated fields like 'total')
        fields = ['men', 'women', 'children', 'non_binary']

        # Human-readable labels for UI display
        labels = {
            'men'       : 'Number of Men',
            'women'     : 'Number of Women',
            'children'  : 'Number of Children',
            'non_binary': 'Number of Non-Binary',
        }

        # UI widgets with validation and styling attributes
        widgets = {
            'men'       : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'women'     : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'children'  : forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
            'non_binary': forms.NumberInput(attrs={'min': 0, 'placeholder': '0', 'class': 'wf-input'}),
        }
