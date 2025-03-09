from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesConfig(AppConfig):
    """
    Configuration class for the categories app.

    Attributes:
        default_auto_field: Primary key field type for models
        name: Python path to the application
        verbose_name: Human-readable app name for display in admin interface
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.categories"
    verbose_name: str = _("Categories")
