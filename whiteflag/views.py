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
from django.http import Http404
from .forms import WhiteFlagForm
from .models import WhiteFlag
from django.contrib.auth.decorators import login_required

from datetime import date

# Maximum capacity constant used in shelter tracking logic
CAPACITY = 80

@login_required
def flow_control(request):
    if request.method == "GET":
        latest_record = WhiteFlag.objects.latest("submitted_at")

        ### Data has been submitted for today ###
        if latest_record.submitted_at.date() == date.today():
            return redirect('whiteflag_edit', pk=latest_record.pk)

        ### No data submitted yet ###
        return blank_page(request)


@login_required
def blank_page(request):
    """Handles creation of new WhiteFlag records.

    - Displays an empty form on GET requests
    - Processes form submission on POST requests
    - Saves valid data to the database
    - Redirects user to edit page after successful submission
    """

    form = WhiteFlagForm() #blank form
    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': None,
    })

@login_required
def handle_submission(request):
    form = WhiteFlagForm(request.POST)
    submission_type = None

    if request.POST.get("record_number") == None: submission_type = "new"
    else: submission_type = "edit"

    # Validate submitted form data before saving
    if form.is_valid():
        if submission_type == "new":
            record = form.save()
            return redirect('edit_page', pk=record.pk)

        if submission_type == "edit":
            pk = request.POST.get("record_number")
            record = get_object_or_404(WhiteFlag, pk=pk)

            record.men = int(request.POST.get("men"))
            record.women = int(request.POST.get("women"))
            record.children = int(request.POST.get("children"))
            record.non_binary = int(request.POST.get("non_binary"))

            record.save()

        # Redirect to edit page for further updates
        return redirect('whiteflag_edit', pk=record.pk)
    raise Http404

@login_required
def edit_page(request, pk):
    """
    Handles editing of existing WhiteFlag records.

    - Retrieves record using primary key (pk)
    - Pre-fills form with existing data
    - Updates record when valid POST data is submitted
    - Saves changes and reloads edit page
    """
    record = get_object_or_404(WhiteFlag, pk=pk) # Retrieve record or return 404 if not found
    form = WhiteFlagForm(instance=record)

    # Render edit page with current record data
    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': record,
    })