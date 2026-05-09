"""
Mainscreen Views

This module controls the main landing page of the UCS system.

It is responsible for:
- Redirecting users to the main screen
- Handling administrator login authentication
- Routing users to shelter selection pages
- Managing basic navigation logic across the system

This acts as the central entry point for user interactions.
"""

from django.http import HttpResponse, HttpResponseRedirect
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required


def HomepageRedirect(request):
    """
    Redirects root URL requests to the mainscreen page.
    Ensures consistent landing page routing.
    """

    return HttpResponseRedirect('/mainscreen/')

@login_required
def mainscreen(request):
    """
    Main application dashboard view.

    Handles:
    - Administrator login validation
    - Shelter selection routing
    - Error messaging for invalid input

    This page serves as the central navigation hub for the UCS system.
    """

    if request.method == 'POST':

        # ---- Administrator Login ----
        if 'admin_login' in request.POST:
            password = request.POST.get('admin_password', '')

            # SECURITY NOTE:
            # Currently uses settings-based password validation.
            # Future improvement: replace with database-driven authentication
            # using AdminSettings model or Django user permissions.


            if password == settings.ADMIN_PANEL_PASSWORD:
                request.session['is_admin'] = True
                return redirect('admin_page_one')
            else:
                messages.error(request, 'Incorrect administrator password.')

        # ------------------------------------------------------------
        # Shelter Selection Routing
        # ------------------------------------------------------------
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

    # Render main dashboard page
    return render(request, 'mainscreen.html')
