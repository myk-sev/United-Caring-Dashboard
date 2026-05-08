from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import ShiftReport
from shelters.models import Shelter, ShelterInputModel

# =========================
# REPORTS PAGE (FILTERING)
# =========================
@login_required
def reports_home(request):

    shelter = request.GET.get('shelter')
    start = request.GET.get('start')
    end = request.GET.get('end')

    shelter_data = ShelterInputModel.objects.all().order_by('-date')
    whiteflag_data = WhiteFlag.objects.all().order_by('-submitted_at')

    if shelter:
        shelter_data = shelter_data.filter(shelter=shelter)

    if start:
        shelter_data = shelter_data.filter(date__gte=start)

    if end:
        shelter_data = shelter_data.filter(date__lte=end)

    return render(request, 'reports.html', {
        'shelter_data': shelter_data,
        'whiteflag_data': whiteflag_data,
        'selected_shelter': shelter,
        'start': start,
        'end': end
    })


# =========================
# EXPORT (ALL DATA + FILTERED)
# =========================
@login_required
def export_all_data(request):

    shelter = request.GET.get('shelter')
    start = request.GET.get('start')
    end = request.GET.get('end')

    shelter_data = ShelterInputModel.objects.all()
    whiteflag_data = WhiteFlag.objects.all()

    # Apply filters
    if shelter:
        shelter_data = shelter_data.filter(shelter=shelter)

    if start:
        shelter_data = shelter_data.filter(date__gte=start)

    if end:
        shelter_data = shelter_data.filter(date__lte=end)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ucs_reports.csv"'

    writer = csv.writer(response)

    # FULL HEADER (ALL YOUR FORM DATA)
    writer.writerow([
        "Type",
        "Date",
        "Shelter",
        "Regular Beds",
        "Respite Beds",
        "Guests On Pass",
        "Hospital",
        "Jail",
        "No Show",
        "Barred",
        "Hold",
        "Record Number",
        "Men",
        "Women",
        "Children",
        "Non Binary",
        "Total",
        "Submitted At"
    ])

    # SHELTER REPORT DATA (FULL)
    for s in shelter_data:
        writer.writerow([
            "Shelter",
            s.date,
            s.shelter,
            s.regular,
            s.respite,
            s.guests,
            s.hospital,
            s.jail,
            s.no_show,
            s.barred,
            s.hold,
            "", "", "", "", "", "", ""
        ])

    # WHITE FLAG DATA
    for w in whiteflag_data:
        writer.writerow([
            "WhiteFlag",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            w.record_number,
            w.men,
            w.women,
            w.children,
            w.non_binary,
            w.total,
            w.submitted_at
        ])

    return response


# =========================
# IMPORT (SAFE + FULL DATA)
# =========================
@login_required
def import_all_data(request):

    if request.method == "POST" and request.FILES.get("file"):

        file = request.FILES["file"]
        decoded = file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded)

        next(reader, None)

        for row in reader:

            # ---- SHELTER FULL DATA ----
            if row[0] == "Shelter":
                try:
                    ShelterInputModel.objects.update_or_create(
                        date=row[1],
                        shelter=row[2],
                        defaults={
                            "regular": int(row[3] or 0),
                            "respite": int(row[4] or 0),
                            "guests": int(row[5] or 0),
                            "hospital": int(row[6] or 0),
                            "jail": int(row[7] or 0),
                            "no_show": int(row[8] or 0),
                            "barred": int(row[9] or 0),
                            "hold": int(row[10] or 0),
                        }
                    )
                except Exception:
                    continue

            # ---- WHITE FLAG ----
            elif row[0] == "WhiteFlag":
                try:
                    WhiteFlag.objects.update_or_create(
                        record_number=row[11],
                        defaults={
                            "men": int(row[12] or 0),
                            "women": int(row[13] or 0),
                            "children": int(row[14] or 0),
                            "non_binary": int(row[15] or 0),
                        }
                    )
                except Exception:
                    continue

    return redirect("/reports/")