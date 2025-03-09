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
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "admin_honeypot",
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",
    "djoser",
    "social_django",
    "taggit",
    "django_filters",
    "djcelery_email",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "cloudinary",
    "django_celery_beat",
    "mptt",
    "django_mptt_admin",
]

LOCAL_APPS = [
    "core_apps.users",
    "core_apps.profiles",
    "core_apps.common",
    "core_apps.categories",
    "core_apps.products",
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


# Internationalization and Localization
USE_TZ = True
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True

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


CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)


# Name of the cookie used for storing access token
COOKIE_NAME = "access"

# Controls how the cookie is sent in cross-site requests
# 'Lax' provides a balance between security and usability
COOKIE_SAMESITE = "Lax"

# Cookie is available for all paths in the domain
COOKIE_PATH = "/"

# Prevents JavaScript access to the cookie, mitigating XSS attacks
COOKIE_HTTPONLY = True

# Only send cookie over HTTPS in production (True), configurable via env var
COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True"


REST_FRAMEWORK = {
    # Specifies the authentication method using custom cookie-based
    # JWT authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core_apps.common.cookie_auth.CookieAuthentication",
    ),
    # Requires users to be authenticated to access API endpoints by default
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    # Enables page number-based pagination for API responses
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    # Adds Django Filter backend for advanced queryset filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    # Sets number of items per page in paginated responses
    "PAGE_SIZE": 10,
    # Rate limiting classes for authenticated and anonymous users
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    # Defines rate limits: anonymous users can make 20 requests/day,
    # authenticated users 400/day
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/day",
        "user": "400/day",
    },
}


# Djoser configuration settings for user authentication and management
DJOSER = {
    # Field used to identify users (UUID in this case)
    "USER_ID_FIELD": "id",
    # Use email instead of username for authentication
    "LOGIN_FIELD": "email",
    # Disable default token model as we're using JWT
    "TOKEN_MODEL": None,
    # Require password confirmation during user creation
    "USER_CREATE_PASSWORD_RETYPE": True,
    # Enable email verification for new accounts
    "SEND_ACTIVATION_EMAIL": True,
    # Send confirmation email when password is changed
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # Require password confirmation during reset
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    # URL pattern for account activation
    "ACTIVATION_URL": "activate/{uid}/{token}",
    # URL pattern for password reset confirmation
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    # Allowed redirect URIs for social authentication
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": getenv("REDIRECT_URIS", "").split(","),
    # Custom serializers for user operations
    "SERIALIZERS": {
        # Custom serializer for user creation
        "user_create": "core_apps.users.serializers.CreateUserSerializer",
        # Custom serializer for current user details
        "current_user": "core_apps.users.serializers.CustomUserSerializer",
    },
}

# JWT configuration settings
SIMPLE_JWT = {
    # Secret key used for signing JWT tokens
    "SIGNING_KEY": getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # Generate new refresh token after refresh
    "ROTATE_REFRESH_TOKENS": True,
    # Field used to identify users in the database
    "USER_ID_FIELD": "id",
    # Claim name for user ID in JWT payload
    "USER_ID_CLAIM": "user_id",
}


# Google OAuth2 client ID from environment variables
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv("GOOGLE_CLIENT_ID")
# Google OAuth2 client secret from environment variables
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv("GOOGLE_CLIENT_SECRET")
# Required OAuth2 scopes for Google authentication
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    # Permission to access user's email
    "https://www.googleapis.com/auth/userinfo.email",
    # Permission to access user's profile information
    "https://www.googleapis.com/auth/userinfo.profile",
    # OpenID Connect authentication
    "openid",
]
# Additional user data fields to fetch from Google
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

# Define the social authentication pipeline
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "core_apps.profiles.pipeline.save_profile",
]

# Define authentication backends for the application
AUTHENTICATION_BACKENDS = (
    # Enable Google OAuth2 authentication using social-auth-app-django
    "social_core.backends.google.GoogleOAuth2",
    # Django's default authentication backend for username/password auth
    "django.contrib.auth.backends.ModelBackend",
)
