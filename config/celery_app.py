import os

from celery import Celery
from django.conf import settings

"""
Celery configuration module.

This module sets up and configures Celery for asynchronous task processing 
in the application. It integrates with Django settings and automatically 
discovers tasks from installed applications.
"""

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# Initialize Celery application
app = Celery("workerfind")

# Configure Celery using Django settings
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix in Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
# This will look for a 'tasks.py' file in each app directory
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
