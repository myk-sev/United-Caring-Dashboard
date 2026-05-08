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
from django.contrib.auth.decorators import login_required

class TestSettingsModel:
    """
    Temporary configuration class used to store shelter capacity values.

    This simulates dynamic shelter settings for:
    - Men's shelter
    - Women's shelter
    - Diversion shelter

    NOTE: This is a simple in-memory structure and not persistent in the database.
    """

    mens_regular = 50
    womens_regular = 40
    diversion_regular = 5
    capacity = -1

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

    # Assign capacity based on selected shelter type
    if (shelter == 'mens'): TestSettingsModel.capacity = TestSettingsModel.mens_regular
    elif (shelter == 'womens'): TestSettingsModel.capacity = TestSettingsModel.womens_regular
    elif (shelter == 'diversion'): TestSettingsModel.capacity = TestSettingsModel.diversion_regular
    #else: raise

    # NOTE: Could add validation for unexpected shelter types

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
            "test_settings_db": TestSettingsModel
        }

    )