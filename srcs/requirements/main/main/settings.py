"""Settings for the project"""
import os
from django.utils.translation import gettext_lazy as _
import environ


env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#u+!b2hbhf$fz#1a=x-dpo!78on7r(%3x9b5y4!ri*p8vtl&v!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = ["localhost", "onur.pythonanywhere.com"]

AUTH_USER_MODEL = 'account.User'

# CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://onur.pythonanywhere.com",
]

CSRF_TRUSTED_ORIGINS = [
    'https://onur.pythonanywhere.com',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'account.backend.CaseInsensitiveEmailBackend',
)

WSGI_APPLICATION = "main.wsgi.application"
ASGI_APPLICATION = "main.asgi.application"

USER_ONLINE_TIMEOUT = 10
USER_LAST_SEEN_TIMEOUT = 60 * 60 * 24 * 7

LOGIN_URL = "account:login"

# WebSocket protocol
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": env('CHANNEL_BACKEND'),
        "CONFIG": {
            "hosts": [(env('CHANNEL_HOST'), env('CHANNEL_PORT'))],
        },
    },
}
"""
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
"""
INSTALLED_APPS = [
#     my party
    'account',
    'chat',
    'friend',
    'tictac',
    'pong',

#     third party
    'daphne',
    'channels',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'whitenoise.runserver_nostatic',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Dil ayarlarını işlemek için
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.middleware.ActiveUserMiddleware',  # local user middleware
    'middleware.middleware.LanguageMiddleware',  # local multiple language middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',  # debug false
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "middleware.middleware.add_variable_to_context",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': env('POSTGRES_ENGINE'),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
}
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/


TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True

BASE_URL = "https://[::]:8000"

DATA_UPLOAD_MEMORY_SIZE = 10485760  # 10 MB

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
]

LANGUAGE_CODE = "en"
USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('tr', _('Turkish')),
]

LANGUAGE_COOKIE_NAME = "django_language"
LANGUAGE_COOKIE_AGE = 31536000
LANGUAGE_REDIRECT = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#zdefault-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
PASSWORD_RESET_TIMEOUT_DAYS = 1
