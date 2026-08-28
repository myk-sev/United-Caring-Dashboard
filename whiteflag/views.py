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
    latest_record = WhiteFlag.objects.first()
    if (
        latest_record
        and timezone.localdate(latest_record.submitted_at) == timezone.localdate()
    ):
        return redirect("whiteflag_edit", pk=latest_record.pk)
    return blank_page(request)


def blank_page(request):
    """Display an empty WhiteFlag form."""
    return render(request, "whiteflag/white_flag.html", {
        "form": WhiteFlagForm(),
        "capacity": get_shelter_capacity('whiteflag')['total_beds'],
        "record": None,
    })


@login_required
def handle_submission(request):
    """Create or update a record from the shared form."""
    if request.method != "POST":
        return redirect("whiteflag")

    record_number = request.POST.get("record_number")
    record = get_object_or_404(WhiteFlag, pk=record_number) if record_number else None
    form = WhiteFlagForm(request.POST, instance=record)
    if form.is_valid():
        record = form.save()
        messages.success(request, f"Record #{record.pk} saved successfully.")
        return redirect("whiteflag_edit", pk=record.pk)

    return render(request, "whiteflag/white_flag.html", {
        "form": form,
        "capacity": get_shelter_capacity('whiteflag')['total_beds'],
        "record": record,
    }, status=400)


@login_required
def edit_page(request, pk):
    """Display an existing WhiteFlag record for editing."""
    record = get_object_or_404(WhiteFlag, pk=pk)
    return render(request, "whiteflag/white_flag.html", {
        "form": WhiteFlagForm(instance=record),
        "capacity": get_shelter_capacity('whiteflag')['total_beds'],
        "record": record,
    })
