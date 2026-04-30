from django.contrib import admin
from django.urls import path, include

import mainscreen.views

urlpatterns = [
    path('', include('mainscreen.urls')),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('reports.urls')),
    path('shelters/', include('shelters.urls')),
    path('white-flag/', include('whiteflag.urls')),
    path('', include('admin_panel.urls')),
]