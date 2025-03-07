from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    """
    Configuration class for the products app.

    This app handles product-related functionality including product management,
    product types, attributes, and product lines.

    Attributes:
        default_auto_field: Primary key field type for models
        name: Python path to the application
        verbose_name: Human-readable app name for display in admin interface
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.products"
    verbose_name: str = _("Products")
