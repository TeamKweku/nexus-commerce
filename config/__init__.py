from .celery_app import app as celery_app

"""
Root configuration package.

This module initializes and exports the Celery application instance for use
throughout the project. The Celery app is configured in celery_app.py and made
available here for Django's auto-discovery mechanism.
"""

__all__ = ("celery_app",)
