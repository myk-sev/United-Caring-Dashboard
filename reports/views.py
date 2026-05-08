"""
Reports Views Module

This module handles all reporting functionality for the UCS system.

It includes:
- Filtering shelter and WhiteFlag data by date and shelter type
- Exporting filtered data to CSV format
- Importing CSV data back into the system
- Data validation and safe parsing of external files

This module represents the core data exchange system of the project.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import csv
from datetime import datetime

from shelters.models import ShelterInputModel, Shelter
from whiteflag.models import WhiteFlag
from .models import ShiftReport

from openpyxl import Workbook  # (kept if you plan XLSX export later)


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

    # -----------------------------
    # Shelter Type Filtering
    # -----------------------------
    if shelter:
        shelter_data = shelter_data.filter(shelter=shelter)

    # -----------------------------
    # Date Range Filtering (Start)
    # -----------------------------
    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            shelter_data = shelter_data.filter(date__gte=start_date)
        except ValueError:
            pass

    # -----------------------------
    # Date Range Filtering (End)
    # -----------------------------
    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            shelter_data = shelter_data.filter(date__lte=end_date)
        except ValueError:
            pass

    return render(request, 'reports.html', {
        'shelter_data': shelter_data,
        'whiteflag_data': whiteflag_data,
        'selected_shelter': shelter,
        'start': start,
        'end': end
    })


# =========================
# EXPORT (CSV - FILTERED)
# =========================
@login_required
def export_all_data(request):
    """
    Exports filtered system data into a CSV file.

    Includes:
    - Shelter intake records
    - WhiteFlag records
    - Applied filters (shelter type and date range)

    Output:
    - Downloadable CSV file for external analysis or editing
    """
    
    shelter = request.GET.get('shelter')
    start = request.GET.get('start')
    end = request.GET.get('end')

    shelter_data = ShelterInputModel.objects.all()
    whiteflag_data = WhiteFlag.objects.all()

    # Shelter filter
    if shelter:
        shelter_data = shelter_data.filter(shelter=shelter)

    # Safe date parsing
    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            shelter_data = shelter_data.filter(date__gte=start_date)
        except ValueError:
            pass

    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            shelter_data = shelter_data.filter(date__lte=end_date)
        except ValueError:
            pass

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ucs_reports.csv"'

    writer = csv.writer(response)

    # -----------------------------
    # CSV HEADER
    # -----------------------------
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

    # =========================
    # SHELTER DATA
    # =========================
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

    # =========================
    # WHITE FLAG DATA
    # =========================
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


# =========================================================
# CSV IMPORT FUNCTION (CORE FEATURE)
# =========================================================
@login_required
def import_all_data(request):
    """
    Imports CSV data into the system.

    Features:
    - Reads uploaded CSV file
    - Separates Shelter and WhiteFlag data
    - Updates or creates records safely
    - Handles malformed rows without crashing system

    Security:
    - Uses try/except blocks to prevent import failures
    - Validates row structure before processing
    """
    
    if request.method == "POST" and request.FILES.get("file"):

        file = request.FILES["file"]
        decoded = file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded)

        next(reader, None)  # skip header

        for row in reader:

            # Guard against broken rows
            if not row or len(row) < 2:
                continue

            # =========================
            # SHELTER IMPORT
            # =========================
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

            # =========================
            # WHITE FLAG IMPORT
            # =========================
            elif row[0] == "WhiteFlag":
                try:
                    WhiteFlag.objects.update_or_create(
                        record_number=row[11],
                        defaults={
                            "men": int(row[12] or 0),
                            "women": int(row[13] or 0),
                            "children": int(row[14] or 0),
                            "non_binary": int(row[15] or 0),
                            "total": int(row[16] or 0),
                        }
                    )
                except Exception:
                    continue

    return redirect("/reports/")
