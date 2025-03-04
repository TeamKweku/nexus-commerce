from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoriesConfig(AppConfig):
    """
    Configuration class for the categories app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.categories"
    verbose_name = _("Categories")
