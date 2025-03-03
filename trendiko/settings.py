"""
Django settings for trendiko project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
WEBSITE_BASE_URL = config("BASE_URL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_DJANGO_HOSTS", cast=Csv())

# Application definition

# add if needed django extensions, django compressor, django celery, django haystack
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    #  Third party apps
    "rest_framework",
    "imagekit",
    "ckeditor",
    "ckeditor_uploader",
    "django_crontab",
    "adminsortable2",
    "nested_admin",
    # Local apps
    "common.apps.CommonConfig",
    "shop.apps.ShopConfig",
    "shop_manager.apps.ShopManagerConfig",
    "cart.apps.CartConfig",
    "stock.apps.StockConfig",
    "facebook.apps.FacebookConfig",
    "analytics.apps.AnalyticsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Local middlewares
    "cart.middleware.CartMiddleware.CartMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = config("ALLOWED_DJANGO_HOSTS", cast=Csv())

ROOT_URLCONF = "trendiko.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # 'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = "trendiko.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if config("USE_SQLITE", default=False, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / config("DATABASE_NAME"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config("DATABASE_NAME"),
            "USER": config("DATABASE_USER"),
            "PASSWORD": config("DATABASE_PASSWORD"),
            "HOST": config("DATABASE_HOST"),
            "PORT": config("DATABASE_PORT"),
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

# REST_FRAMEWORK = {
#     "EXCEPTION_HANDLER": "common.utils.global_exception_handler",
# }

# Loggers
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_warn": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "warn.log",
            "formatter": "detailed",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "error.log",
            "formatter": "detailed",
        },

        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "info.log",
            "formatter": "detailed",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "detailed",
        },
    },
    "formatters": {
        "detailed": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "loggers": {
        "": {
            "handlers": ["file_warn", "file_error", "file_info", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

if DEBUG:
    LOGGING["loggers"][""]["handlers"].append("console")

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Skopje"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collectstatic"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"

# CKEDITOR
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_FORCE_JPEG_COMPRESSION = True

CKEDITOR_CONFIGS = {
    "default": {
        "height": 300,
        "width": 1000,
        "toolbar": "Custom",
        "toolbar_Custom": [
            [
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "NumberedList",
                "BulletedList",
            ],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["Image", "Link", "Maximize"],
            ["Undo", "Redo", "Html5video"],
        ],
        "extraPlugins": ",".join(
            [
                "uploadimage",
                "dialogui",
                "dialog",
                "button",
                "widgetselection",
                "toolbar",
                "notification",
                "clipboard",
                "lineutils",
                "widget",
                "html5video",
            ]
        ),
    }
}
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRONJOBS = [
    ("0 * * * *", "facebook.cron.update_facebook_catalogue_feed"),
    ("0 0 */28 * *", "facebook.cron.refresh_facebook_access_token"),
    ("0 0 * * *", "cart.cron.make_carts_abandoned"),
    ("0 4 * * *", "analytics.cron.create_campaign_summaries"),
]

# Celery configuration
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = config("CELERY_ACCEPT_CONTENT", cast=Csv())
CELERY_TASK_SERIALIZER = config("CELERY_TASK_SERIALIZER")

INVOICES_DIR = BASE_DIR / "invoices"
EXCHANGE_RATE_API_KEY = config("EXCHANGE_RATE_API_KEY")
# USE_THOUSAND_SEPARATOR = True
