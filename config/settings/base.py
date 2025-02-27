from datetime import timedelta
from os import getenv, path
from pathlib import Path

import cloudinary
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# Base directory of the application would be in the core_apps
APPS_DIR = BASE_DIR / "core_apps"

# Local env directory for development purposes only.
local_env_file = path.join(BASE_DIR, ".envs", ".env.local")
if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",
    "djoser",
    "social_django",
    "taggit",
    "django_filters",
    "djcelery_email",
    "cloudinary",
    "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.users",
    "core_apps.profiles",
    "core_apps.common",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": getenv("POSTGRES_PORT"),
    }
}

# Using argon password hashers from Django Docs
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Accra"

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAGGIT_CASE_INSENSITIVE = True

AUTH_USER_MODEL = "users.User"

# Use Django's timezone settings for Celery if timezone support is enabled
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

# Redis URL for message broker
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
# Redis URL for storing results
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
# Only accept JSON-serialized content
CELERY_ACCEPT_CONTENT = ["application/json"]
# Use JSON for serializing task messages
CELERY_TASK_SERIALIZER = "json"
# Use JSON for serializing results
CELERY_RESULT_SERIALIZER = "json"
# Maximum number of times to retry connecting to the result backend
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

# Enable sending of task-sent events
CELERY_TASK_SEND_SENT_EVENT = True
# Include additional task result metadata
CELERY_RESULT_EXTENDED = True

# Always retry connecting to the result backend if connection fails
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

# Hard time limit for tasks (5 minutes)
CELERY_TASK_TIME_LIMIT = 5 * 60

# Soft time limit for tasks (1 minute) - allows for cleanup before hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 60

# Use Django database as the scheduler backend
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Enable sending task events from workers
CELERY_WORKER_SEND_TASK_EVENTS = True

# Periodic task definitions
CELERY_BEAT_SCHEDULE = {
    "update-reputations-every-day": {
        "task": "update_all_reputations",  # Task name to execute
        "schedule": timedelta(days=1),  # Run once per day
    }
}


CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)
