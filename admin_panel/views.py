from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from shelters.models import ShelterInputModel
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
    data_retrieval = ShelterInputModel.objects.last()

    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == 'POST' and 'change_password' in request.POST:
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

    return render(
        request,
        'admin_panel/admin_page_two.html',
        {#"db_entry": data_retrieval,
         "test": "diversion",
         "test_db": temp})

@login_required
def admin_logout(request):
    """Clear admin session and return to main screen."""
    request.session.pop('is_admin', None)
    return redirect('mainscreen')

class temp:
    id = 5
    date = "2026-12-12"
    shelter = "diversion"
    regular_occupied = 10
    guests = 21
    hospital = 31
    jail = 41
    no_show = 10
    barred = 7
    hold = 5
    respite = 10
    men = 40
    women = 50
    children = 2
    non_binary = 100