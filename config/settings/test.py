from .base import *  # noqa

DEBUG = True

# Use SQLite for tests instead of PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # Run tests with in-memory database for speed
    }
}

# Define SECRET_KEY for testing
SECRET_KEY = "test-secret-key-12345"

# Define ADMIN_URL for testing
ADMIN_URL = "admin/"

# Make tests faster by using simple password hashing
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Disable Celery in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable email sending during tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
