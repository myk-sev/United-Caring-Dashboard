from django.contrib import admin
from django.urls import path, include

import mainscreen.views

urlpatterns = [
    path('', mainscreen.views.mainscreen),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('reports.urls')),
    path('shelters/', include('shelters.urls')),
    path('mainscreen/', include('mainscreen.urls')),
    path('white-flag/', include('whiteflag.urls')),
    path('', include('admin_panel.urls')),
]