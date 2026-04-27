from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    create_superuser()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')

def create_superuser():
    import os
    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.environ["DJANGO_SUPERUSER_USERNAME"]
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
    password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )