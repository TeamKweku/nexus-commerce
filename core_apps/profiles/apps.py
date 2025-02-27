from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    """
    Configuration class for the profiles app.

    This class defines app-specific configurations and initializes
    signal handlers when the app is ready.
    """

    # Use BigAutoField as the primary key type for all models
    default_auto_field = "django.db.models.BigAutoField"

    # Full Python path to the application
    name = "core_apps.profiles"

    # Human-readable name for the app (translatable)
    verbose_name = _("Profiles")

    def ready(self) -> None:
        """
        Callback when app is ready to be used.

        Imports the signals module to register signal handlers.
        The noqa comment prevents flake8 from flagging the import
        as unused since it's needed for signal registration.
        """
        import core_apps.profiles.signals  # noqa: F401
