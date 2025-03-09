from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa
from .base import BASE_DIR

# Production env directory for production purposes only.
production_env_file = path.join(BASE_DIR, ".envs", ".env.production")
if path.isfile(production_env_file):
    load_dotenv(production_env_file)

SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
)

DEBUG = False

SITE_NAME = getenv("SITE_NAME")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ALLOWED_HOSTS = [""]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = getenv.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 518400
SECURE_HSTS_INCLUDE_SUBDOMAINS = getenv.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = getenv.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = getenv.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# Honeypot Production Settings
HONEYPOT_EMAIL_ADMINS = True
HONEYPOT_NOTIFY_ADMINS = True

# Admin notification email settings for honeypot
ADMINS = [
    ("Security Team", getenv("SECURITY_TEAM_EMAIL")),
]

# Email configuration for security notifications
EMAIL_SUBJECT_PREFIX = "[Nexus Commerce Security] "


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(name)-12s %(asctime)s "
                "%(module)s %(process)d %(thread)d %(message)s"
            )
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
