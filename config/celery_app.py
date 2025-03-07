import os

from celery import Celery
from celery.schedules import crontab
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
app = Celery("nexuscommerce")

# Configure Celery using Django settings
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix in Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
# This will look for a 'tasks.py' file in each app directory
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "check-low-stock-daily": {
        "task": "check_low_stock_levels",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    "clean-abandoned-carts-weekly": {
        "task": "clean_abandoned_carts",
        "schedule": crontab(0, 0, day_of_week="monday"),  # Weekly on Monday
    },
    "daily-sales-report": {
        "task": "generate_daily_sales_report",
        "schedule": crontab(hour=0, minute=30),  # Daily at 00:30
    },
    "monthly-system-cleanup": {
        "task": "cleanup_old_sessions",
        "schedule": crontab(0, 0, day_of_month="1"),  # Monthly on the 1st
    },
}
