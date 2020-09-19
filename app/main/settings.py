"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
import raven
from urllib.parse import urlparse, unquote
from os.path import splitext
from uuid import uuid4


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

DEBUG = False
if os.environ.get("DEBUG") == "True":
    DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')
if SECRET_KEY is None:
    if DEBUG:
        SECRET_KEY = '+q=28spl&0qh*e_h$x8t4yp1t*avz8rgc9z_8s*ho0eag18$pn'
    else:
        raise EnvironmentError("Please specify a SECRET_KEY in your environment")

ALLOWED_HOSTS = ['*']

if not DEBUG:
    SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'cms.apps.CmsConfig',
    'sortedm2m',
    'tags_input',
    'rest_framework',
    'django_filters',
    'tz_detect',
    'rest_framework.authtoken',
    'raven.contrib.django.raven_compat',
    'oauth2_provider',
    'emoji_picker',
    's3direct',
    'admin_object_actions',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'app/templates'],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.environ.get('DATABASE_URL') is not None:
    DATABASES = {
        'default': dj_database_url.config()
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/admin/login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL[1:])

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

aws_url = os.environ.get('S3_MEDIA_URL')
if aws_url is not None:
    aws_creds = urlparse(aws_url)
    DEFAULT_FILE_STORAGE = 'main.custom_storages.S3BotoRandomNameStorage'
    AWS_ACCESS_KEY_ID = unquote(aws_creds.username)
    AWS_SECRET_ACCESS_KEY = unquote(aws_creds.password)
    AWS_STORAGE_BUCKET_NAME = aws_creds.hostname
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_REGION_NAME = 'eu-central-1'
    AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.amazonaws.com'

    custom_domain = os.environ.get('S3_CUSTOM_DOMAIN')
    if custom_domain:
        AWS_S3_CUSTOM_DOMAIN = custom_domain
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL[1:])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

TAGS_INPUT_MAPPINGS = {
    'cms.ReportTag': {
        'field': 'name',
        'create_missing': True,
    },
    'cms.Genre': {
        'field': 'name',
        'create_missing': False,
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.apps.StandardPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

TZ_DETECT_COUNTRIES = ('DE', 'FR', 'GB', 'US', 'CN', 'IN', 'JP', 'BR', 'RU')

sentry_dsn =  os.environ.get('SENTRY_DSN')

if sentry_dsn is not None:
    RAVEN_CONFIG = {
        'dsn': sentry_dsn,
    }

OAUTH2_PROVIDER = {
    'SCOPES': {
        'user': 'User profile',
    },
}

# S3Direct
def generate_filename(fn):
    name, ext = splitext(fn)
    return f'{name}-{str(uuid4())}{ext}'


S3DIRECT_DESTINATIONS = {
    'default': {
        # REQUIRED
        'key': generate_filename,

        # OPTIONAL
        'auth': lambda u: u.is_staff,  # Default allow anybody to upload
        'cache_control': 'max-age=2592000',  # Default no cache-control
        'content_disposition': 'attachment',  # Default no content disposition
        'content_length_range': (0, 5000000),  # Default allow any size
        'allow_existence_optimization': True,  # Don't re-upload files that exist on S3 already
    },
}
