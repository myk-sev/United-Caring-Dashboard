"""
WhiteFlag Views

This module handles the WhiteFlag workflow in the UCS system,
including creating and editing WhiteFlag records.

The system allows authenticated users to:
- Submit new WhiteFlag entries
- Edit existing entries
- Track capacity-related data for shelter management

Access is restricted to logged-in users only for security purposes.
"""

from django.shortcuts import get_object_or_404, redirect, render
from .forms import WhiteFlagForm
from .models import WhiteFlag
from django.contrib.auth.decorators import login_required

# Maximum capacity constant used in shelter tracking logic
CAPACITY = 80

@login_required
def white_flag(request):
     
    """
    Handles creation of new WhiteFlag records.

    - Displays an empty form on GET requests
    - Processes form submission on POST requests
    - Saves valid data to the database
    - Redirects user to edit page after successful submission
    """
     
    if request.method == 'POST':
        form = WhiteFlagForm(request.POST)

        # Validate submitted form data before saving
        if form.is_valid():
            record = form.save()

            # Redirect to edit page for further updates
            return redirect('white_flag_edit', pk=record.pk)
    else:
        # Initialize empty form for new entry
        form = WhiteFlagForm()

    # Render form page with capacity information
    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': None,
    })


@login_required
def white_flag_edit(request, pk):
    """
    Handles editing of existing WhiteFlag records.

    - Retrieves record using primary key (pk)
    - Pre-fills form with existing data
    - Updates record when valid POST data is submitted
    - Saves changes and reloads edit page
    """

    # Retrieve record or return 404 if not found
    record = get_object_or_404(WhiteFlag, pk=pk)

    if request.method == 'POST':
        form = WhiteFlagForm(request.POST, instance=record)

        # Validate and update existing record
        if form.is_valid():
            record = form.save()
            return redirect('white_flag_edit', pk=record.pk)
    else:
        # Load form with existing record data
        form = WhiteFlagForm(instance=record)

    # Render edit page with current record data
    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': record,
    })