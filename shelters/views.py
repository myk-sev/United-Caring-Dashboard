from django.shortcuts import render
from django.http import HttpResponseRedirect
from shelters.form import ShelterInputForm
from shelters.models import ShelterInputModel

def shelters_home(request):
    shelter = request.GET.get('shelter', '')

    if request.method == "POST":
        form_data = ShelterInputForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return HttpResponseRedirect('/shelters/')

    form = ShelterInputForm(initial={'shelter': shelter})
    return render(request, 'shelters.html', {'form': form, 'shelter': shelter})