import uuid

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.users.managers import UserManager


class UsernameValidator(validators.RegexValidator):
    """
    Custom validator for usernames.

    Ensures usernames only contain letters, numbers, and specific symbols
    (dot, @, +, -) to prevent security issues and maintain consistency.
    """

    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain "
        "letters, numbers, a dot, "
        "@ symbol, + symbol and a hyphen "
    )
    flag = 0


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model uses email as the primary identifier for authentication while
    maintaining username for display purposes. It adds UUID-based identification
    and separates the primary key (pkid) from the public ID (id) for security.

    Attributes:
        pkid: Auto-incrementing big integer primary key (not exposed publicly)
        id: UUID that serves as the public identifier for the user
        first_name: User's first name (required)
        last_name: User's last name (required)
        email: User's email address (unique, used for authentication)
        username: User's username (unique, validated format)
    """

    # Primary keys and identifiers
    pkid = models.BigAutoField(
        primary_key=True,
        editable=False,
        help_text=_("Auto-incrementing primary key (not exposed publicly)"),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("Public identifier for the user"),
    )

    # Personal information
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=60,
        help_text=_("User's first name"),
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=60,
        help_text=_("User's last name"),
    )

    # Authentication fields
    email = models.EmailField(
        verbose_name=_("Email Address"),
        unique=True,
        db_index=True,
        help_text=_("Email address used for authentication"),
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=60,
        unique=True,
        validators=[UsernameValidator],
        help_text=_("Username for display purposes"),
    )

    # Configure authentication fields
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # Field used for authentication
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # Use custom manager for user creation and management
    objects = UserManager()

    class Meta:
        """
        Model metadata options.

        Defines verbose names for admin interface and default ordering.
        """

        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]  # Most recent users first

    @property
    def get_full_name(self) -> str:
        """
        Returns the user's full name by combining first and last name.

        Returns:
            str: The user's full name with any leading/trailing whitespace
            removed
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
