"""
ASGI Configuration for Shelter System Project

This module serves as the entry point for ASGI-compatible servers
to run the UCS Django application.

ASGI (Asynchronous Server Gateway Interface) enables support for:
- Asynchronous request handling
- WebSocket communication (if used in future extensions)
- Modern deployment environments

This file is used during application deployment.
"""

import os

from django.core.asgi import get_asgi_application

# Set default settings module for ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shelter_system.settings')

# Create ASGI application callable for the server
application = get_asgi_application()
