"""
Accounts Views

This module handles user authentication for the UCS system.

It includes:
- User login functionality
- User logout functionality

This module uses Django’s built-in authentication system.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """
    Handles user login authentication.

    Workflow:
    - Validates username and password using Django authentication
    - Logs user in if credentials are valid
    - Redirects to homepage upon success
    - Displays error message if authentication fails
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    """
    Logs out the current user.

    Clears session data and redirects to login page.
    """

    logout(request)
    request.session.flush()
    return redirect('/login/')
