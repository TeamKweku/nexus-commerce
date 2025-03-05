from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    """
    Configuration class for the products app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.products"
    verbose_name = _("Products")
