"""
Shelters Views

This module handles the main shelter intake workflow for the UCS system.

It manages:
- Selecting shelter types (men, women, diversion)
- Assigning capacity settings based on selection
- Processing shelter intake form submissions
- Saving shelter records to the database
- Redirecting users after successful submission

This view supports both GET and POST requests for interactive form handling.
"""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from shelters.form import ShelterInputForm
from shelters.models import get_shelter_capacity
from django.contrib.auth.decorators import login_required

@login_required
def shelters_home(request):
    """
    Handles the main shelters intake page.

    Responsibilities:
    - Detect selected shelter type (GET or POST)
    - Assign correct capacity based on selection
    - Process form submission for shelter intake
    - Validate and save form data
    - Redirect user after successful submission
    """

    # Determine selected shelter type from request
    if request.method == "POST": shelter = request.POST.get("shelter", "")
    else: shelter = request.GET.get("shelter", "")

    capacity = get_shelter_capacity(shelter) if shelter in {'mens', 'womens', 'diversion'} else {
        'total_beds': 0,
        'respite_beds': 0,
    }

    # Handle form submission (POST request)
    if request.method == "POST":
        form_data = ShelterInputForm(request.POST)

        # Validate form before saving to database
        if form_data.is_valid():
            record = form_data.save(commit=False)
            record.save()

            # Redirect to same page with selected shelter type
            return HttpResponseRedirect(f"/shelters/?shelter={record.shelter}")
        else:
            # Debugging output for form validation issues
            print("FORM ERRORS:", form_data.errors)
            print("POST DATA:", request.POST)

    # Initialize form with preselected shelter value
    form = ShelterInputForm(initial={'shelter': shelter})

    # Render shelters page with context data
    return render(
        request,
        'shelters.html',
        {
            'form': form,
            'shelter': shelter,
            'capacity': capacity['total_beds'],
            'respite_capacity': capacity['respite_beds'],
        }

    )
