from django.shortcuts import render

def home(request):
    return render(request, 'mainscreen.html')