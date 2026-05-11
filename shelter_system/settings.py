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
import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (used for secure configuration)
load_dotenv(BASE_DIR / ".env")


# Base directory reference (used for file paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

### Production Variables ###
SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
DEBUG = os.environ.get("DEBUG")

# Allowed hosts for deployment
ALLOWED_HOSTS = ["united-caring-dashboard.onrender.com"]



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
    #'mainscreen',
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
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
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
ADMIN_PANEL_PASSWORD = "admin1234"


# ---------------------------------------------------
# Static Files
# ---------------------------------------------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
