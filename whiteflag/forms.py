from django import forms
from .models import WhiteFlag


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
