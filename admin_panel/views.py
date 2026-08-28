"""
Admin Panel Views

This module controls all administrative functionality within the UCS system.

It provides:
- Admin authentication and session handling
- Dashboard analytics (Page 1)
- Record search and modification tools (Page 2)
- Password management
- Admin logout functionality

This module is restricted to authenticated admin users only.
"""

from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.crypto import constant_time_compare

from shelters.form import ShelterInputForm
from shelters.models import DEFAULT_CAPACITIES, Shelter, ShelterInputModel, get_shelter_capacity
from whiteflag.forms import WhiteFlagForm
from whiteflag.models import WhiteFlag


def capacity_settings():
    return {name: get_shelter_capacity(name) for name in DEFAULT_CAPACITIES}


def utilization(records, capacity, fields):
    values = list(records.values_list(*fields))
    if not values or capacity <= 0:
        return 0
    return round(100 * sum(sum(row) for row in values) / (capacity * len(values)))


# -----------------------------------------------------------
# Admin Login
# -----------------------------------------------------------
@login_required
def admin_login(request): #Creates a login page for the admin panel. If the password is correct, it sets a session variable to indicate that the user is an admin and redirects to the first admin page. If the password is incorrect, it shows an error message.
    """Standalone Admin login page."""
    if request.session.get('is_admin'):
        return redirect('admin_page_one')

    if request.method == 'POST':
        password = request.POST.get('admin_password', '')

        if (
            settings.ADMIN_PANEL_PASSWORD
            and constant_time_compare(password, settings.ADMIN_PANEL_PASSWORD)
        ):
            request.session['is_admin'] = True
            return redirect('admin_page_one')
        else:
            messages.error(request, 'Incorrect administrator password.')

    return render(request, 'admin_panel/admin_login.html')


# -----------------------------------------------------------
# Admin Dashboard Page 1 (Analytics)
# -----------------------------------------------------------
@login_required
def admin_page_one(request):
    """Administration Page 1 of 2 — Daily Records / Charts."""
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    
    capacities = capacity_settings()
    since = timezone.localdate() - timedelta(days=29)
    mens_records = ShelterInputModel.objects.filter(shelter='mens')
    womens_records = ShelterInputModel.objects.filter(shelter='womens')
    diversion_records = ShelterInputModel.objects.filter(shelter='diversion')
    whiteflag_records = WhiteFlag.objects.all()

    # Retrieve the chronologically latest record for each shelter type.
    mens_data = mens_records.order_by('-date', '-id').first()
    womens_data = womens_records.order_by('-date', '-id').first()
    diversion_data = diversion_records.order_by('-date', '-id').first()
    whiteflag_data = WhiteFlag.objects.first()

    mens_regular_total = capacities['mens']['total_beds']
    mens_respite_total = capacities['mens']['respite_beds']
    womens_regular_total = capacities['womens']['total_beds']
    womens_respite_total = capacities['womens']['respite_beds']
    diversion_regular_total = capacities['diversion']['total_beds']
    whiteflag_total = capacities['whiteflag']['total_beds']

    # Calculate available capacity for each shelter
    mens_regular_available = max(0, mens_regular_total - (mens_data.regular if mens_data else 0))
    mens_respite_available = max(0, mens_respite_total - (mens_data.respite if mens_data else 0))
    womens_regular_available = max(0, womens_regular_total - (womens_data.regular if womens_data else 0))
    womens_respite_available = max(0, womens_respite_total - (womens_data.respite if womens_data else 0))
    diversion_regular_available = max(0, diversion_regular_total - (diversion_data.regular if diversion_data else 0))
    
    # WhiteFlag calculations
    whiteflag_occupied = whiteflag_data.total if whiteflag_data else 0
    whiteflag_available = max(0, whiteflag_total - whiteflag_occupied)

    return render(request, 'admin_panel/admin_page_one.html', {
        'mens_data': mens_data,
        'mens_regular_total': mens_regular_total,
        'mens_respite_total': mens_respite_total,
        'mens_regular_available': mens_regular_available,
        'mens_respite_available': mens_respite_available,
        'mens_utilization': utilization(
            mens_records.filter(date__gte=since),
            mens_regular_total + mens_respite_total,
            ('regular', 'respite'),
        ),
        'womens_data': womens_data,
        'womens_regular_total': womens_regular_total,
        'womens_respite_total': womens_respite_total,
        'womens_regular_available': womens_regular_available,
        'womens_respite_available': womens_respite_available,
        'womens_utilization': utilization(
            womens_records.filter(date__gte=since),
            womens_regular_total + womens_respite_total,
            ('regular', 'respite'),
        ),
        'diversion_data': diversion_data,
        'diversion_regular_total': diversion_regular_total,
        'diversion_regular_available': diversion_regular_available,
        'diversion_utilization': utilization(
            diversion_records.filter(date__gte=since),
            diversion_regular_total,
            ('regular',),
        ),
        'whiteflag_data': whiteflag_data,
        'whiteflag_total': whiteflag_total,
        'whiteflag_available': whiteflag_available,
        'whiteflag_occupied': whiteflag_occupied,
        'whiteflag_utilization': utilization(
            whiteflag_records.filter(submitted_at__date__gte=since),
            whiteflag_total,
            ('total',),
        ),
    })


# -----------------------------------------------------------
# Admin Dashboard Page 2 (Search + Modify Records)
# -----------------------------------------------------------
@login_required
def admin_page_two(request):
    """Administration Page 2 of 2 — Alter Records / Settings."""
    record = None #ensure default display is empty
    record_type = None

    if not request.session.get('is_admin'):
        return redirect('admin_login')

    context = {'capacities': capacity_settings()}

    if request.method == 'POST':

        # -------------------------------------------------------
        # App Login Password Change Functionality
        # -------------------------------------------------------
        if 'change_capacities' in request.POST:
            fields = {
                'mens': ('mens_regular_capacity', 'mens_respite_capacity'),
                'womens': ('womens_regular_capacity', 'womens_respite_capacity'),
                'diversion': ('diversion_regular_capacity', None),
                'whiteflag': ('whiteflag_capacity', None),
            }
            try:
                updates = {
                    name: {
                        'total_beds': int(request.POST[regular]),
                        'respite_beds': int(request.POST[respite]) if respite else 0,
                    }
                    for name, (regular, respite) in fields.items()
                }
            except (KeyError, TypeError, ValueError):
                messages.error(request, 'All capacities must be whole numbers.')
            else:
                if any(value < 0 for item in updates.values() for value in item.values()):
                    messages.error(request, 'Capacities cannot be negative.')
                else:
                    for name, values in updates.items():
                        Shelter.objects.update_or_create(name=name, defaults=values)
                    messages.success(request, 'Shelter capacities updated.')
            return redirect('admin_page_two')

        elif 'change_login_password' in request.POST:

            username = request.POST.get('target_username', '').strip()
            new_pw1 = request.POST.get('login_new_password1', '')
            new_pw2 = request.POST.get('login_new_password2', '')

            User = get_user_model()

            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                messages.error(request, 'Username not found.')
                return redirect('admin_page_two')

            if new_pw1 != new_pw2:
                messages.error(request, 'New passwords do not match.')

            elif len(new_pw1) < 4:
                messages.error(request, 'New password is too short.')

            else:
                user.set_password(new_pw1)
                user.save()

                messages.success(
                    request,
                    f'Password successfully changed for {username}.'
                )
        # -------------------------------------------------------
        # Record Search Functionality
        # -------------------------------------------------------
        elif "search_records" in request.POST:
            search_input_id = request.POST.get('search_input_id', '').strip()
            search_input_date = request.POST.get('search_input_date', '')
            search_input_shelter = request.POST.get('search_input_shelter', '')

            if not search_input_id and not search_input_date:
                messages.error(request, 'Enter a record number or date.')
                return redirect('admin_page_two')

            if search_input_id and not search_input_id.isdigit():
                messages.error(request, 'Record number must be numeric.')
                return redirect('admin_page_two')

            search_date = None
            if not search_input_id:
                try:
                    search_date = date.fromisoformat(search_input_date)
                except ValueError:
                    messages.error(request, 'Enter a valid record date.')
                    return redirect('admin_page_two')

            if search_input_shelter == 'whiteflag':
                records = WhiteFlag.objects.all()
                record = (
                    records.filter(record_number=search_input_id).first()
                    if search_input_id
                    else records.filter(submitted_at__date=search_date).first()
                )
                record_type = 'whiteflag'
            else:
                records = ShelterInputModel.objects.filter(shelter=search_input_shelter)
                record = (
                    records.filter(id=search_input_id).first()
                    if search_input_id
                    else records.filter(date=search_date).order_by('-id').first()
                )
                record_type = 'shelter'

            if record is None:
                messages.error(request, 'No matching record was found.')
                return redirect('admin_page_two')

            context.update(record=record, record_type=record_type)
            return render(request, 'admin_panel/admin_page_two.html', context)

        # -------------------------------------------------------
        # Record Modification Functionality
        # -------------------------------------------------------
        elif "alter_records" in request.POST:
            record_type = request.POST.get('record_type', 'shelter')
            old_id = request.POST.get("old_id")

            if not old_id or not old_id.isdigit():
                messages.error(request, 'Select a valid record before saving.')
                return redirect('admin_page_two')

            if record_type == 'whiteflag':
                old_record = WhiteFlag.objects.filter(record_number=old_id).first()
                if old_record is None:
                    messages.error(request, 'The White Flag record no longer exists.')
                    return redirect('admin_page_two')

                form_data = WhiteFlagForm(request.POST, instance=old_record)

                if form_data.is_valid():
                    form_data.save()
                    messages.success(request, 'White Flag record updated.')
                    return redirect('admin_page_two')

                else:
                    record = old_record
                    messages.error(request, 'Correct the invalid White Flag values.')

            else:
                old_record = ShelterInputModel.objects.filter(id=old_id).first()
                if old_record is None:
                    messages.error(request, 'The shelter record no longer exists.')
                    return redirect('admin_page_two')

                form_data = ShelterInputForm(request.POST, instance=old_record)

                if form_data.is_valid():
                    try:
                        form_data.instance.date = date.fromisoformat(request.POST.get('date', ''))
                    except ValueError:
                        record = old_record
                        record_type = 'shelter'
                        messages.error(request, 'Enter a valid record date.')
                    else:
                        form_data.save()
                        messages.success(request, 'Shelter record updated.')
                        return redirect('admin_page_two')

                else:
                    record = old_record
                    record_type = 'shelter'
                    messages.error(request, 'Correct the invalid shelter values.')

    context.update(record=record, record_type=record_type)
    return render(request, 'admin_panel/admin_page_two.html', context)

# -----------------------------------------------------------
# Admin Logout
# -----------------------------------------------------------
@login_required
def admin_logout(request):
    """Clear admin session and return to main screen."""
    request.session.pop('is_admin', None)
    return redirect('mainscreen')
