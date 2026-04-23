from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from shelters.models import ShelterInputModel

@never_cache
@login_required
def home(request):
    form_retrieval = ShelterInputModel.objects.last()


    shelter = None
    if form_retrieval:
        shelter = form_retrieval.shelter

    return render(request, "dashboard.html", {
        "shelter": shelter
    })