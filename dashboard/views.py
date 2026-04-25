from django.shortcuts import render
from shelters.models import ShelterInputModel

def home(request):
    form_retrieval = ShelterInputModel.objects.last()
    shelter = form_retrieval.shelter
    return render(request, 'dashboard.html', {"shelter": shelter})