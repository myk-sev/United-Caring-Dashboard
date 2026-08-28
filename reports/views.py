"""Filter, export, and import shelter and White Flag reports."""

import csv
from datetime import datetime
from io import StringIO
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag


SHELTER_NAMES = {"mens", "womens", "diversion"}
CSV_HEADERS = [
    "Type", "Date", "Shelter", "Regular Beds", "Respite Beds",
    "Guests On Pass", "Hospital", "Jail", "No Show", "Barred", "Hold",
    "Record Number", "Men", "Women", "Children", "Non Binary", "Total",
    "Submitted At",
]
MAX_IMPORT_SIZE = 5 * 1024 * 1024


def parse_filter_date(value, label):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{label} must be a valid date.") from exc


def filtered_records(params):
    shelter = params.get("shelter", "")
    if shelter not in SHELTER_NAMES | {"", "whiteflag"}:
        raise ValueError("Select a valid shelter.")

    start = parse_filter_date(params.get("start", ""), "Start date")
    end = parse_filter_date(params.get("end", ""), "End date")
    if start and end and start > end:
        raise ValueError("Start date cannot be after end date.")

    shelter_data = ShelterInputModel.objects.all().order_by("-date", "-id")
    whiteflag_data = WhiteFlag.objects.all().order_by("-submitted_at")

    if shelter == "whiteflag":
        shelter_data = shelter_data.none()
    elif shelter:
        shelter_data = shelter_data.filter(shelter=shelter)
        whiteflag_data = whiteflag_data.none()

    if start:
        shelter_data = shelter_data.filter(date__gte=start)
        whiteflag_data = whiteflag_data.filter(submitted_at__date__gte=start)
    if end:
        shelter_data = shelter_data.filter(date__lte=end)
        whiteflag_data = whiteflag_data.filter(submitted_at__date__lte=end)

    return shelter_data, whiteflag_data


@login_required
def reports_home(request):
    try:
        shelter_data, whiteflag_data = filtered_records(request.GET)
    except ValueError as exc:
        messages.error(request, str(exc))
        shelter_data = ShelterInputModel.objects.none()
        whiteflag_data = WhiteFlag.objects.none()

    filters = {
        key: request.GET.get(key, "")
        for key in ("shelter", "start", "end")
        if request.GET.get(key)
    }
    return render(request, "reports.html", {
        "shelter_data": shelter_data,
        "whiteflag_data": whiteflag_data,
        "selected_shelter": request.GET.get("shelter", ""),
        "start": request.GET.get("start", ""),
        "end": request.GET.get("end", ""),
        "export_query": urlencode(filters),
    })


@login_required
def export_all_data(request):
    try:
        shelter_data, whiteflag_data = filtered_records(request.GET)
    except ValueError as exc:
        return HttpResponse(str(exc), content_type="text/plain", status=400)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="ucs_reports.csv"'
    writer = csv.writer(response)
    writer.writerow(CSV_HEADERS)

    for record in shelter_data:
        writer.writerow([
            "Shelter", record.date, record.shelter, record.regular,
            record.respite, record.guests, record.hospital, record.jail,
            record.no_show, record.barred, record.hold, "", "", "", "", "",
            "", "",
        ])

    for record in whiteflag_data:
        writer.writerow([
            "WhiteFlag", "", "", "", "", "", "", "", "", "", "",
            record.record_number, record.men, record.women, record.children,
            record.non_binary, record.total, record.submitted_at,
        ])

    return response


def parse_count(row, column, row_number):
    try:
        value = int((row.get(column) or "0").strip())
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: {column} must be a whole number.") from exc
    if value < 0:
        raise ValueError(f"Row {row_number}: {column} cannot be negative.")
    return value


def parse_import(file):
    if not file.name.lower().endswith(".csv"):
        raise ValueError("Select a CSV file.")
    if file.size > MAX_IMPORT_SIZE:
        raise ValueError("CSV files must be 5 MB or smaller.")

    try:
        text = file.read().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("The CSV file must use UTF-8 encoding.") from exc

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames != CSV_HEADERS:
        raise ValueError("The CSV header does not match the UCS export format.")

    records = []
    for row_number, row in enumerate(reader, 2):
        if None in row:
            raise ValueError(f"Row {row_number}: too many columns.")
        if not any((value or "").strip() for value in row.values()):
            continue

        record_type = (row.get("Type") or "").strip()
        if record_type == "Shelter":
            try:
                date = datetime.strptime(row["Date"].strip(), "%Y-%m-%d").date()
            except (AttributeError, ValueError) as exc:
                raise ValueError(f"Row {row_number}: Date must use YYYY-MM-DD.") from exc
            shelter = (row.get("Shelter") or "").strip()
            if shelter not in SHELTER_NAMES:
                raise ValueError(f"Row {row_number}: select a valid shelter.")
            counts = {
                field: parse_count(row, column, row_number)
                for field, column in (
                    ("regular", "Regular Beds"), ("respite", "Respite Beds"),
                    ("guests", "Guests On Pass"), ("hospital", "Hospital"),
                    ("jail", "Jail"), ("no_show", "No Show"),
                    ("barred", "Barred"), ("hold", "Hold"),
                )
            }
            records.append(("shelter", date, shelter, counts))
        elif record_type == "WhiteFlag":
            record_number = parse_count(row, "Record Number", row_number)
            if not record_number:
                raise ValueError(f"Row {row_number}: Record Number is required.")
            counts = {
                field: parse_count(row, column, row_number)
                for field, column in (
                    ("men", "Men"), ("women", "Women"),
                    ("children", "Children"), ("non_binary", "Non Binary"),
                )
            }
            total = sum(counts.values())
            total_text = (row.get("Total") or "").strip()
            if total_text and parse_count(row, "Total", row_number) != total:
                raise ValueError(f"Row {row_number}: Total does not match the demographic counts.")
            submitted_text = (row.get("Submitted At") or "").strip()
            submitted_at = parse_datetime(submitted_text)
            if submitted_text and submitted_at is None:
                raise ValueError(f"Row {row_number}: Submitted At is not a valid timestamp.")
            if submitted_at and timezone.is_naive(submitted_at):
                submitted_at = timezone.make_aware(submitted_at)
            records.append(("whiteflag", record_number, submitted_at, counts))
        else:
            raise ValueError(f"Row {row_number}: Type must be Shelter or WhiteFlag.")

    if not records:
        raise ValueError("The CSV file contains no data rows.")
    return records


def save_import(records):
    shelter_count = whiteflag_count = 0
    with transaction.atomic():
        for record_type, identity, detail, counts in records:
            if record_type == "shelter":
                record = ShelterInputModel.objects.filter(
                    date=identity, shelter=detail
                ).order_by("id").first()
                if record:
                    for field, value in counts.items():
                        setattr(record, field, value)
                    record.save(update_fields=counts)
                else:
                    record = ShelterInputModel.objects.create(shelter=detail, **counts)
                    ShelterInputModel.objects.filter(pk=record.pk).update(date=identity)
                shelter_count += 1
            else:
                record, _ = WhiteFlag.objects.update_or_create(
                    record_number=identity, defaults=counts
                )
                if detail:
                    WhiteFlag.objects.filter(pk=record.pk).update(submitted_at=detail)
                whiteflag_count += 1
    return shelter_count, whiteflag_count


@login_required
def import_all_data(request):
    if request.method != "POST" or not request.FILES.get("file"):
        messages.error(request, "Select a CSV file to import.")
        return redirect("reports")

    try:
        shelter_count, whiteflag_count = save_import(
            parse_import(request.FILES["file"])
        )
    except (csv.Error, ValueError) as exc:
        messages.error(request, f"Import failed: {exc} No records were changed.")
    else:
        messages.success(
            request,
            f"Imported {shelter_count} shelter and {whiteflag_count} White Flag records.",
        )
    return redirect("reports")
