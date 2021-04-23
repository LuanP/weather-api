"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

APP_NAME = config("APP_NAME", default="weather-api")

OPENWEATHERMAP_API_URL = config(
    "OPENWEATHERMAP_API_URL", default="https://api.openweathermap.org/data/2.5/onecall"
)
OPENWEATHERMAP_API_KEY = config("OPENWEATHERMAP_API_KEY")
OPENWEATHERMAP_EXCLUDE = config(
    "OPENWEATHERMAP_EXCLUDE", cast=Csv(), default="currently,minutely,hourly,alerts"
)
OPENWEATHERMAP_UNITS = config("OPENWEATHERMAP_UNITS", default="metric")


INSTALLED_APPS = [
    "graphene_django",
    "app.contrib.locations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

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

WSGI_APPLICATION = "app.wsgi.application"

# GraphQL

GRAPHENE = {"SCHEMA": "app.schema.schema"}
GRAPHIQL = config("GRAPHIQL", cast=bool, default=False)
if GRAPHIQL:
    INSTALLED_APPS = [
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "django.contrib.staticfiles",
    ] + INSTALLED_APPS

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("WEATHER_DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("WEATHER_DB_NAME"),
        "USER": config("WEATHER_DB_USERNAME"),
        "PASSWORD": config("WEATHER_DB_PASSWORD"),
        "HOST": config("WEATHER_DB_HOST"),
        "PORT": config("WEATHER_DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("CACHE_LOCATION"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": config("CACHE_PREFIX", default="weather"),
    }
}

CACHE_TTL = config("CACHE_TTL", cast=int, default=60 * 30)  # default TTL: 30 minutes


PYTHON_ENV = config("PYTHON_ENV", default="production")


# Development only

if PYTHON_ENV == "test":
    FREEZE_TIME = "2021-04-22 20:00:00"
    INSTALLED_APPS += ["django_nose"]

    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

    NOSE_ARGS = [
        "--with-coverage",
        "--cover-erase",
        "--cover-package=app",
        "--cover-html-dir=htmlcov",
        "--where=tests",
    ]

    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test-db"}}
