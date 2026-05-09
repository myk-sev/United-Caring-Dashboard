"""
Accounts Views

This module handles user authentication for the UCS system.

It includes:
- User login functionality
- User logout functionality
- Automatic creation of a default superuser (development use only)

This module uses Django’s built-in authentication system.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """
    Handles user login authentication.

    Workflow:
    - Ensures a default superuser exists (development helper)
    - Validates username and password using Django authentication
    - Logs user in if credentials are valid
    - Redirects to homepage upon success
    - Displays error message if authentication fails
    """

    create_superuser()

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

def create_superuser():
    """
    Automatically creates a default superuser account if one does not exist.

    NOTE:
    - This is intended for development/testing only.
    - Credentials are pulled from environment variables.
    - Should be removed or replaced in production with secure admin setup.
    """

    import os
    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    # Create superuser only if it does not already exist
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )