# ocr_project/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-example-secret-key-12345'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.136.90.160']  # Allow local requests from browser

INSTALLED_APPS = [
    # Django Built-in Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ocr_app',

    # CORS App (REQUIRED)
    'corsheaders',

    # Your custom app
    'ocr_app.apps.OcrAppConfig',
]

MIDDLEWARE = [
    # CORS middleware MUST be at the top
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ocr_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ocr_project.wsgi.application'

# MySQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ocrdb',
        'USER': 'root',
        'PASSWORD': 'Y9025975941@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔥 Allow frontend to access Django
CORS_ALLOW_ALL_ORIGINS = True

# =======================================================
# 🌟 MEDIA FILE CONFIGURATION (CRITICAL ADDITION) 🌟
# =======================================================

# The URL prefix for media files (uploaded images)
MEDIA_URL = '/media/'

# The absolute filesystem path to the directory that will hold user-uploaded files.
# This points to a folder named 'media' in your project root.
MEDIA_ROOT = BASE_DIR / 'media'