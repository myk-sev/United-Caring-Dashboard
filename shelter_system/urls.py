from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reports/', include('reports.urls')),
    path('shelters/', include('shelters.urls')),
    #path('', include('mainscreen.urls')),
    path('white-flag/', include('whiteflag.urls')),
    path('', include('admin_panel.urls')),
]