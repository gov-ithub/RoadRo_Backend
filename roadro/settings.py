"""
Django settings for roadro project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL not configured")

MEDIA_STORAGE_FOLDER = os.getenv("MEDIA_STORAGE_PATH")
if not MEDIA_STORAGE_FOLDER:
    raise Exception("Invalid MEDIA_STORAGE_PATH value")

if os.path.exists(MEDIA_STORAGE_FOLDER) is False:
    raise Exception("The %s folder doesn't exist" % MEDIA_STORAGE_FOLDER)

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("The REDIS_URL value is not set in the environment")

REDIS_POOL_MAX_CONNECTIONS = os.getenv("REDIS_POOL_MAX_CONNECTIONS", 30)

TICKET_LIMITER_EXPIRE_TIME = os.getenv("TICKET_LIMITER_EXPIRE_TIME", 10)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = bytes([int(c, 16) for c in os.getenv("DJANGO_SECRET_KEY", "").split('x') if c != ""])
if not SECRET_KEY or len(SECRET_KEY) < 50:
    raise Exception("Invalid or missing DJANGO_SECRET_KEY. Needs to have 50+ bytes")

AES_IV = bytes([int(c, 16) for c in os.getenv("AES_IV", "").split('x') if c != ""])
if not AES_IV or len(AES_IV) != 16:
    raise Exception("Invalid or missing AES_IV. Needs to have 16 bytes")

PLATFORM = os.getenv("PLATFORM")
if not PLATFORM or PLATFORM.lower() not in ("local", "dev", "staging", "prod"):
    raise Exception("PLATFORM needs to have one of the following values: local, dev, staging, prod")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if PLATFORM.lower() == "local" else False

# for now leave *. to be changed when we get a domain
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'tickets',
    'imgserv',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roadro.middleware.SpringInitializer'
]

ROOT_URLCONF = 'roadro.urls'

WSGI_APPLICATION = 'roadro.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'