"""
Django settings for geodjango_tutorial project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import socket
# from django.core.management.utils import get_random_secret_key
from pathlib import Path
from decouple import config
import dj_database_url

# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, ‘static/js’, ‘serviceworker.js’)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default=None)
DEPLOY_SECURE = config('DEPLOY_SECURE', default=False, cast=bool)

DEBUG = config('DEBUG', default=False, cast=bool)

if DEPLOY_SECURE:
    DEBUG = False
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
    CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])
else:
    DEBUG = True
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'leaflet',
    'django.contrib.gis',
    'world.apps.WorldConfig',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geodjango_tutorial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (53.0, -8.0),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
    'SCALE': None,
    'OPACITY': 0.5,
}

WSGI_APPLICATION = 'geodjango_tutorial.wsgi.application'

if os.environ.get('CONDA_PREFIX','').startswith('/opt'):
    DATABASES = {'default': config('DATABASE_DOCKER', default=None, cast=dj_database_url.parse)}
else:
    DATABASES = {'default': config('DATABASE_LOCAL', default=None, cast=dj_database_url.parse)}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'world.User'
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if socket.gethostname() == "Sophies-MacBook-Pro-2.local":
    DATABASES["default"]["HOST"] = "localhost"
    DATABASES["default"]["PORT"] = 25432            # docker_config.POSTGIS_PORT
else:
    DATABASES["default"]["HOST"] = "wmap-postgis"   #"wmap-postgis" # f"{docker_config.AWMASSIGN}-postgis"
    DATABASES["default"]["PORT"] = 5432

# PWA_APP_NAME = 'Fuel Finder'
# PWA_APP_DESCRIPTION = "Fuel Finder PWA"
# PWA_APP_THEME_COLOR = '#000000'
# PWA_APP_BACKGROUND_COLOR = '#ffffff'
# PWA_APP_DISPLAY = 'standalone'
# PWA_APP_SCOPE = '/'
# PWA_APP_ORIENTATION = 'any'
# PWA_APP_START_URL = '/'
# PWA_APP_STATUS_BAR_COLOR = 'default'
# PWA_APP_ICONS = [
#     {
#         'src': 'static/images/icon-160x160.png',
#         'sizes': '160x160'
#     }
# ]
# PWA_APP_ICONS_APPLE = [
#     {
#         'src': 'static/images/icon-160x160.png',
#         'sizes': '160x160'
#     }
# ]
# PWA_APP_SPLASH_SCREEN = [
#     {
#         'src': 'static/images/icon.png',
#         'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
#     }
# ]
# PWA_APP_DIR = 'ltr'
# PWA_APP_LANG = 'en-US'