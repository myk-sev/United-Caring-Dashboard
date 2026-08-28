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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from shelters.form import ShelterInputForm
from shelters.models import ShelterInputModel, get_shelter_capacity

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

    shelter = request.POST.get('shelter', '') if request.method == 'POST' else request.GET.get('shelter', '')
    if shelter not in {'mens', 'womens', 'diversion'}:
        return redirect('mainscreen')

    capacity = get_shelter_capacity(shelter)
    record = None

    # Handle form submission (POST request)
    if request.method == "POST":
        record_id = request.POST.get('record_id')
        if record_id:
            if not record_id.isdigit():
                messages.error(request, 'Select a valid record before saving.')
                return redirect(f'/shelters/?shelter={shelter}')
            record = ShelterInputModel.objects.filter(pk=record_id, shelter=shelter).first()
            if record is None:
                messages.error(request, 'The shelter record no longer exists.')
                return redirect(f'/shelters/?shelter={shelter}')

        form_data = ShelterInputForm(request.POST, instance=record)

        # Validate form before saving to database
        if form_data.is_valid():
            record = form_data.save()
            messages.success(request, f'Record #{record.pk} saved successfully.')
            return redirect(f'/shelters/?shelter={record.shelter}')

        form = form_data

    else:
        if request.GET.get('new') != '1':
            record = ShelterInputModel.objects.filter(
                shelter=shelter,
                date=timezone.localdate(),
            ).order_by('-id').first()
        form = ShelterInputForm(instance=record, initial={'shelter': shelter})

    def available(field, total):
        try:
            occupied = int(form[field].value() or 0)
        except (TypeError, ValueError):
            occupied = 0
        return max(0, total - occupied)

    # Render shelters page with context data
    return render(
        request,
        'shelters.html',
        {
            'form': form,
            'shelter': shelter,
            'capacity': capacity['total_beds'],
            'respite_capacity': capacity['respite_beds'],
            'regular_open': available('regular', capacity['total_beds']),
            'respite_open': available('respite', capacity['respite_beds']),
            'record': record,
        }

    )
