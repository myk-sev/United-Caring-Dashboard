from django.shortcuts import render
from django.http import HttpResponseRedirect

def shelters_home(request):
    if request.method == "POST":
        # Here you can access form data using request.POST
        shelter = request.POST.get("shelter")
        regular_occupied = request.POST.get("regular_occupied")
        # ... handle other fields
        # Redirect or save to database
        return HttpResponseRedirect('/shelters/')  # redirect after submission

    return render(request, 'shelters.html')