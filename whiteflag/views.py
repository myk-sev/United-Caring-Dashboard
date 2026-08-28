"""Create and edit authenticated WhiteFlag occupancy records."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from shelters.models import get_shelter_capacity

from .forms import WhiteFlagForm
from .models import WhiteFlag


@login_required
def flow_control(request):
    """Open today's record, or display a blank form."""
    latest_record = WhiteFlag.objects.filter(
        submitted_at__date=timezone.localdate()
    ).first()
    if latest_record:
        return redirect("whiteflag_edit", pk=latest_record.pk)
    return blank_page(request)


def blank_page(request):
    """Display an empty WhiteFlag form."""
    return render(request, "whiteflag/white_flag.html", page_context(WhiteFlagForm()))


def page_context(form, record=None):
    """Build the shared page state from the configured capacity."""
    capacity = get_shelter_capacity("whiteflag")["total_beds"]
    total = record.total if record else 0
    return {
        "form": form,
        "capacity": capacity,
        "availability": max(0, capacity - total),
        "record": record,
    }


@login_required
def handle_submission(request):
    """Create or update a record from the shared form."""
    if request.method != "POST":
        return redirect("whiteflag")

    record_number = request.POST.get("record_number")
    record = (
        get_object_or_404(WhiteFlag, pk=record_number)
        if record_number
        else WhiteFlag.objects.filter(submitted_at__date=timezone.localdate()).first()
    )
    form = WhiteFlagForm(request.POST, instance=record)
    if form.is_valid():
        record = form.save()
        messages.success(request, f"Record #{record.pk} saved successfully.")
        return redirect("whiteflag_edit", pk=record.pk)

    return render(
        request,
        "whiteflag/white_flag.html",
        page_context(form, record),
        status=400,
    )


@login_required
def edit_page(request, pk):
    """Display an existing WhiteFlag record for editing."""
    record = get_object_or_404(WhiteFlag, pk=pk)
    return render(
        request,
        "whiteflag/white_flag.html",
        page_context(WhiteFlagForm(instance=record), record),
    )
