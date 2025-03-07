from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    """
    Configuration class for the profiles app.

    Defines app-specific configurations and initializes signal handlers.

    Attributes:
        default_auto_field: Primary key field type for models
        name: Python path to the application
        verbose_name: Human-readable app name
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.profiles"
    verbose_name = _("Profiles")

    def ready(self) -> None:
        """
        Perform initialization tasks when app is ready.

        Imports and registers signal handlers for profile creation.

        Returns:
            None
        """
        import core_apps.profiles.signals  # noqa: F401
