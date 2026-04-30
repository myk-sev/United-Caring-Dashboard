from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # form_retrieval = ShelterInputModel.objects.last()
    # shelter = form_retrieval.shelter
    # return render(request, 'dashboard.html', {"shelter": shelter})
    return render(request, 'dashboard.html')
