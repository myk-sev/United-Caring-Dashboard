"""
WSGI Configuration for Shelter System Project

This module serves as the entry point for WSGI-compatible web servers
to run the UCS Django application in a production environment.

WSGI (Web Server Gateway Interface) is used to connect the Django
application to web servers such as Gunicorn or Apache.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shelter_system.settings')

# Create WSGI application callable for the web server
application = get_wsgi_application()
