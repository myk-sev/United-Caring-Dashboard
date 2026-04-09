from django.shortcuts import render

def reports_home(request):
    return render(request, 'reports.html')