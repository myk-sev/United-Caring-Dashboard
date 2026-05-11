"""
Django Settings Configuration for Shelter System Project

This file defines the global configuration for the UCS Django application.

It controls:
- Installed applications
- Middleware stack
- Database configuration
- Authentication settings
- Template configuration
- Localization settings
- Static file handling

WARNING:
This file contains sensitive configuration values and should be protected
in production environments.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

PRODUCTION = False

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (used for secure configuration)
load_dotenv(BASE_DIR / ".env")


# Base directory reference (used for file paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4q35w89iwpaf%c=5tvz6=65*i_$zcxmybvqllv-ip9kotw$350'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG: # Productions settings for cookies and redirects
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    REFERRER_POLICY = "same-origin"
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allowed hosts for deployment (empty in development)
ALLOWED_HOSTS = []
if PRODUCTION:
    ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]


# ---------------------------------------------------
# Application Definition
# ---------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom project applications
    'accounts',
    'dashboard',
    'reports',
    'shelters',
    'mainscreen',
    'whiteflag',
    'admin_panel',
]

# ---------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shelter_system.urls'

# Authentication redirect settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = '/login/'

# ---------------------------------------------------
# Template Configuration
# ---------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # <-- Add this
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shelter_system.wsgi.application'


# ---------------------------------------------------
# Database Configuration
# ---------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------------------------------------------
# Password Validation
# ---------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ---------------------------------------------------
# Internationalization
# ---------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago' #'UTC'

USE_I18N = True

USE_TZ = True

# Custom admin panel configuration
ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD")


# ---------------------------------------------------
# Static Files
# ---------------------------------------------------

STATIC_URL = 'static/'