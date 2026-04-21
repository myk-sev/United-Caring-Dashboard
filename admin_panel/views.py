from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


def admin_page_one(request):
    """Administration Page 1 of 2 — Daily Records / Charts."""
    if not request.session.get('is_admin'):
        return redirect('mainscreen')
    return render(request, 'admin_panel/admin_page_one.html')


def admin_page_two(request):
    """Administration Page 2 of 2 — Alter Records / Settings."""
    if not request.session.get('is_admin'):
        return redirect('mainscreen')

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

    return render(request, 'admin_panel/admin_page_two.html')


def admin_logout(request):
    """Clear admin session and return to main screen."""
    request.session.pop('is_admin', None)
    return redirect('mainscreen')
