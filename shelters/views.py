from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from shelters.form import ShelterInputForm
from shelters.models import ShelterInputModel
from django.contrib.auth.decorators import login_required

@login_required
def shelters_home(request):
    if request.method == "POST":
        form_data = ShelterInputForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            form_retrieval = ShelterInputModel.objects.first()
            print(form_retrieval.shelter)
            # username = form.cleaned_data["username"]
            # shelter = form.cleaned_data["shelter"]
            # regular_occupied = form.cleaned_data["regular_occupied"]
            # regular_open = form.cleaned_data["regular_open"]
            # guests_on_pass = form.cleaned_data["guests_on_pass"]
            # hospital = form.cleaned_data["hospital"]
            # jail = form.cleaned_data["jail"]
            # nc_ns = form.cleaned_data["nc_ns"]
            # barred = form.cleaned_data["barred"]
            # hold = form.cleaned_data["hold"]
            # respite_occupied = form.cleaned_data["respite_occupied"]
            # respite_open = form.cleaned_data["respite_open"]
            # guests_on_pass = form.cleaned_data["guests_on_pass"]
        return HttpResponseRedirect('/shelters/')  # redirect after submission

    return render(request, 'shelters.html')