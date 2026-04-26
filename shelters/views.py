from django.shortcuts import render
from django.http import HttpResponseRedirect
from shelters.form import ShelterInputForm

class TestSettingsModel:
    mens_regular = 50
    womens_regular = 40
    diversion_regular = 30
    capacity = -1

def shelters_home(request):
    selected = request.GET.get('selected', '')
    if (selected == 'mens'): TestSettingsModel.capacity = TestSettingsModel.mens_regular
    elif (selected == 'womens'): TestSettingsModel.capacity = TestSettingsModel.womens_regular
    elif (selected == 'diversion'): TestSettingsModel.capacity = TestSettingsModel.diversion_regular
    else: raise

    if request.method == "POST":
        form_data = ShelterInputForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return HttpResponseRedirect('/shelters/')

    form = ShelterInputForm(initial={'shelter': selected})
    return render(
        request,
        'shelters.html',
        {
            'form': form,
            'selected': selected,
            "test_settings_db": TestSettingsModel
        }

    )