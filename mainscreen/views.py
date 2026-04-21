#from django.shortcuts import render
from django.http import HttpResponse
import os

#from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


def mainscreen(request):
    """
    Main screen — shown to all users without login.
    Handles two Go buttons:
      1. Shelter dropdown  → routes to the selected shelter's submit page
      2. Administrator Login password → validates and routes to admin_page_one
    """

    if request.method == 'POST':

        # ---- Administrator Login ----
        if 'admin_login' in request.POST:
            password = request.POST.get('admin_password', '')

            # ----------------------------------------------------------------
            # COLLABORATOR NOTE:
            # Replace the settings check below with DB lookup:
            #   from admin_panel.models import AdminSettings
            #   config = AdminSettings.objects.first()
            #   if password == config.admin_password:
            # ----------------------------------------------------------------

            if password == settings.ADMIN_PANEL_PASSWORD:
                request.session['is_admin'] = True
                return redirect('admin_page_one')
            else:
                messages.error(request, 'Incorrect administrator password.')

        # ---- Shelter dropdown Go ----
        elif 'shelter_go' in request.POST:
            shelter = request.POST.get('shelter_select', '')
            if shelter == 'mens':
                return redirect('shelters')      # adjust name to match your shelters url
            elif shelter == 'womens':
                return redirect('shelters')      # adjust when separate womens view exists
            elif shelter == 'diversion':
                return redirect('shelters')      # adjust when separate diversion view exists
            else:
                messages.error(request, 'Please select a shelter.')

    return render(request, 'mainscreen.html')
