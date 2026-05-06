from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from shelters.models import ShelterInputModel
from shelters.form import ShelterInputForm
from whiteflag.models import WhiteFlag
from whiteflag.forms import WhiteFlagForm
from django.contrib.auth.decorators import login_required
from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag


@login_required
def admin_login(request): #Creates a login page for the admin panel. If the password is correct, it sets a session variable to indicate that the user is an admin and redirects to the first admin page. If the password is incorrect, it shows an error message.
    """Standalone Admin login page."""
    if request.session.get('is_admin'):
        return redirect('admin_page_one')

    if request.method == 'POST':
        password = request.POST.get('admin_password', '')

        if password == settings.ADMIN_PANEL_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_page_one')
        else:
            messages.error(request, 'Incorrect administrator password.')

    return render(request, 'admin_panel/admin_login.html')

@login_required
def admin_page_one(request):
    """Administration Page 1 of 2 — Daily Records / Charts."""
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    
    mens_data = ShelterInputModel.objects.filter(shelter='mens').last()
    womens_data = ShelterInputModel.objects.filter(shelter='womens').last()
    diversion_data = ShelterInputModel.objects.filter(shelter='diversion').last()
    whiteflag_data = WhiteFlag.objects.first()
    
    mens_regular_total = 50
    mens_respite_total = 7
    womens_regular_total = 22
    womens_respite_total = 4
    diversion_regular_total = 5
    whiteflag_total = 80

    mens_regular_available = mens_regular_total - mens_data.regular if mens_data else 0
    mens_respite_available = mens_respite_total - mens_data.respite if mens_data else 0
    womens_regular_available = womens_regular_total - womens_data.regular if womens_data else 0
    womens_respite_available = womens_respite_total - womens_data.respite if womens_data else 0
    diversion_regular_available = diversion_regular_total - diversion_data.regular if diversion_data else 0
    whiteflag_occupied = whiteflag_data.total if whiteflag_data else 0
    whiteflag_available = whiteflag_total - whiteflag_occupied if whiteflag_data else 0

    return render(request, 'admin_panel/admin_page_one.html', {
        'mens_data': mens_data,
        'mens_regular_available': mens_regular_available,
        'mens_respite_available': mens_respite_available,
        'womens_data': womens_data,
        'womens_regular_available': womens_regular_available,
        'womens_respite_available': womens_respite_available,
        'diversion_data': diversion_data,
        'diversion_regular_available': diversion_regular_available,
        'whiteflag_data': whiteflag_data,
        'whiteflag_available': whiteflag_available,
        'whiteflag_occupied': whiteflag_occupied,
    })


@login_required
def admin_page_two(request):
    """Administration Page 2 of 2 — Alter Records / Settings."""
    record = None #ensure default display is empty
    record_type = None

    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == 'POST':
        if 'change_password' in request.POST:
            old_pw  = request.POST.get('old_password', '')
            new_pw1 = request.POST.get('new_password1', '')
            new_pw2 = request.POST.get('new_password2', '')

            if old_pw != settings.ADMIN_PANEL_PASSWORD:
                messages.error(request, 'Old password is incorrect.')
            elif new_pw1 != new_pw2:
                messages.error(request, 'New passwords do not match.')
            elif len(new_pw1) < 4:
                messages.error(request, 'New password is too short (minimum 4 characters).')
            else:
                settings.ADMIN_PANEL_PASSWORD = new_pw1
                messages.success(request, 'Password updated successfully.')

        elif "search_records" in request.POST:
            search_input_id = request.POST.get('search_input_id', '')
            search_input_date = request.POST.get('search_input_date', '')
            search_input_shelter = request.POST.get('search_input_shelter', '')

            if search_input_shelter == 'whiteflag':
                if search_input_id != "":
                    record = WhiteFlag.objects.get(record_number=int(search_input_id))

                else:
                    record = WhiteFlag.objects.filter(submitted_at__date=search_input_date).first()

                record_type = 'whiteflag'

            else:
                if search_input_id != "":
                    record = ShelterInputModel.objects.get(id=int(search_input_id))
                else:
                    record = ShelterInputModel.objects.filter(date=search_input_date).get(shelter=search_input_shelter)

                record_type = 'shelter'
            return render(request, 'admin_panel/admin_page_two.html', {"record": record, "record_type": record_type})

        elif "alter_records" in request.POST:
            record_type = request.POST.get('record_type', 'shelter')
            old_id = request.POST.get("old_id")

            if record_type == 'whiteflag':
                old_record = WhiteFlag.objects.get(record_number=old_id)
                form_data = WhiteFlagForm(request.POST, instance=old_record)

                if form_data.is_valid():
                    form_data.save()
                    record = None
                    record_type = None

                else:
                    record = old_record

            else:
                old_record = ShelterInputModel.objects.get(id=old_id)
                old_record.delete()
                form_data = ShelterInputForm(request.POST)

                if form_data.is_valid():
                    record = form_data.save(commit=False)
                    record.save()
                    record = None
                    record_type = None

                else:
                    print("FORM ERRORS:", form_data.errors)
                    print("POST DATA:", request.POST)
                    record = old_record
                    record_type = 'shelter'

    return render(
        request,
    'admin_panel/admin_page_two.html',
    {"record": record, "record_type": record_type}
    )

@login_required
def admin_logout(request):
    """Clear admin session and return to main screen."""
    request.session.pop('is_admin', None)
    return redirect('mainscreen')
