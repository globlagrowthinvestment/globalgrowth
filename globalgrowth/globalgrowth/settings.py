"""
Django settings for globalgrowth project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l+d&tgimr+nho=i-=88=r#q60@g@^l+(^1g9h5s04(a03z93ha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'f6c3-102-209-18-30.ngrok-free.app',
    '105.27.122.14',
    'corsheaders',
    '52.41.36.82',
    '54.191.253.12',
    '44.226.122.3'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'landing',
    'auth_app',
    'dashboard',
    'checkout',
    'my_profile',
    'guide',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
# trusted origin for this case ngrok
CSRF_TRUSTED_ORIGINS = ['https://f6c3-102-209-18-30.ngrok-free.app']

ROOT_URLCONF = 'globalgrowth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'globalgrowth/templates')],
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

WSGI_APPLICATION = 'globalgrowth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'globalgrowth',
        'USER': 'globalgrowth',
        'PASSWORD': 'kali',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
import os
from django.core.management.utils import get_random_secret_key

# ... other settings ...

# Use environment variable for the ngrok URL, defaulting to localhost
#NGROK_URL = os.environ.get('NGROK_URL', 'http://localhost:8000')

# M-Pesa settings
MPESA_CONSUMER_KEY = 'nJ2LBFFdwW5aNftzGj1dwoBajDLqwSieiHQtXaoBKDyXWR7h'
MPESA_CONSUMER_SECRET = 'Obu2axIXXE6IuwW6elUxLMwM9fKYepQOhBmEeAjg5nUAm67ELtmdLExdSUstF9pr'
MPESA_SHORTCODE = '174379'  # Use your actual shortcode
MPESA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Use your actual passkey
MPESA_CALLBACK_URL = '29b2-105-27-122-14.ngrok-free.app'
#MPESA_CALLBACK_URL = f"{NGROK_URL}/checkout/mpesa-callback/"

# For development, you can use a randomly generated secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# Allow the ngrok domain in ALLOWED_HOSTS
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'globalgrowth', 'static'),
]
# this setting is for development, on production we shall change it to the exact origins
CORS_ALLOW_ALL_ORIGINS = True  
CORS_ALLOW_CREDENTIALS = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
