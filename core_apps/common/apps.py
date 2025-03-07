from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    """
    Configuration class for the common app.

    This app provides shared functionality used across the project,
    including base models and utilities.

    Attributes:
        default_auto_field: Primary key field type for models
        name: Python path to the application
        verbose_name: Human-readable app name for display in admin interface
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.common"
    verbose_name: str = _("Common")
