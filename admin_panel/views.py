from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from shelters.models import ShelterInputModel
from shelters.form import ShelterInputForm
from django.contrib.auth.decorators import login_required

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
    return render(request, 'admin_panel/admin_page_one.html')

@login_required
def admin_page_two(request):
    """Administration Page 2 of 2 — Alter Records / Settings."""
    record = None #ensure default display is empty

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
            
            if search_input_id != "":
                record = ShelterInputModel.objects.get(id=int(search_input_id))
            else:
                record = ShelterInputModel.objects.filter(date=search_input_date).get(shelter=search_input_shelter)

            return render( request, 'admin_panel/admin_page_two.html', {"record": record})
        elif "alter_records" in request.POST:
            old_id = request.POST.get("old_id")
            old_record = ShelterInputModel.objects.get(id=old_id)
            old_record.delete()

            form_data = ShelterInputForm(request.POST)

            if form_data.is_valid():
                record = form_data.save(commit=False)
                record.save()

                record = None
            else:
                print("FORM ERRORS:", form_data.errors)
                print("POST DATA:", request.POST)

    return render(
        request,
        'admin_panel/admin_page_two.html',
        {"record": record}
    )

@login_required
def admin_logout(request):
    """Clear admin session and return to main screen."""
    request.session.pop('is_admin', None)
    return redirect('mainscreen')
