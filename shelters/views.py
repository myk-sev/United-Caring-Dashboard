from django.shortcuts import render
from django.http import HttpResponseRedirect
from shelters.form import ShelterInputForm
from shelters.models import ShelterInputModel

class TestSettingsModel:
    mens_capacity_regular = 50
    womens_capacity_regular = 40
    diversion_capacity_regular = 30

def shelters_home(request):
    shelter = request.GET.get('shelter', '')

    if request.method == "POST":
        form_data = ShelterInputForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return HttpResponseRedirect('/shelters/')

    form = ShelterInputForm(initial={'shelter': shelter})
    return render(
        request,
        'shelters.html',
        {
            'form': form,
            'shelter': shelter,
            "test_settings_db": TestSettingsModel
        }

    )