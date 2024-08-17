"""
Django settings for media_management project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x((c@b#zs)ctzzdy_&e9c_*pe(8w-%mr+*yvsif#6qxc(#56*t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "backends_engine.authentication.StaticTokenAuthentication",
    ],
    "EXCEPTION_HANDLER": "media_management.exception_handler.custom_exception_handler",
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "backends_engine",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "media_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "media_management.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TODO:Akash Load this from .env file
API_STATIC_TOKEN = os.getenv('API_STATIC_TOKEN', '12345abcde67890fghij09876klmnop54321')


# Logger configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Formatters
FORMATTERS = {
    "verbose": {
        "format": "{levelname} TIME: {asctime:s} MODULE: {module} LINENO: {lineno:d} MESSAGE: {message}",
        "style": "{",
    },
    "simple": {
        "format": "{levelname} TIME: {asctime:s} MODULE: {module} LINENO: {lineno:d} MESSAGE: {message}",
        "style": "{",
    },
}

# Handlers
HANDLERS = {
    "debug_handler": {
        "class": "media_management.custom_log_handlers.DateRotatingFileHandler",
        "base_filename": os.path.join(BASE_DIR, "logs/debug/", "debug_log"),
        "when": "midnight",
        "backupCount": 30,
        "formatter": "verbose",
        "encoding": "utf-8",
    },
    "info_handler": {
        "class": "media_management.custom_log_handlers.DateRotatingFileHandler",
        "base_filename": os.path.join(BASE_DIR, "logs/info/", "info_log"),
        "when": "midnight",
        "backupCount": 30,
        "formatter": "verbose",
        "encoding": "utf-8",
    },
    "error_handler": {
        "class": "media_management.custom_log_handlers.DateRotatingFileHandler",
        "base_filename": os.path.join(BASE_DIR, "logs/error/", "error_log"),
        "when": "midnight",
        "backupCount": 30,
        "formatter": "simple",
        "encoding": "utf-8",
    },
}

# Loggers
LOGGERS = {
    "debug": {
        "handlers": ["debug_handler"],
        "level": "DEBUG",
        "propagate": False,
    },
    "info": {
        "handlers": ["info_handler"],
        "level": "INFO",
        "propagate": False,
    },
    "error": {
        "handlers": ["error_handler"],
        "level": "ERROR",
        "propagate": False,
    },
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS,
    "handlers": HANDLERS,
    "loggers": LOGGERS,
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR + "/" + "media"

# Settings for video upload limits
MAX_VIDEO_SIZE_MB = os.getenv('MAX_VIDEO_SIZE_MB', 25)
MIN_VIDEO_DURATION_SEC = os.getenv('MIN_VIDEO_DURATION_SEC', 5)
MAX_VIDEO_DURATION_SEC = os.getenv('MAX_VIDEO_DURATION_SEC', 300)

SITE_URL = os.getenv('SITE_URL', 'http://127.0.0.1:8000')

# SMTP email backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "******"
EMAIL_HOST_PASSWORD = "******"
