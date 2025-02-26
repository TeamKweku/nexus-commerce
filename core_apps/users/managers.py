from typing import Any, Dict, Optional

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_email_address(email: str) -> None:
    """
    Validate email format using Django's built-in validator.

    Args:
        email: String containing the email address to validate

    Raises:
        ValidationError: If the email format is invalid
    """
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address"))


class UserManager(DjangoUserManager):
    """
    Custom user manager extending Django's UserManager with enhanced
    functionality.

    This manager provides methods for creating regular users and superusers with
    required email validation and proper password hashing. It enforces business
    rules such as requiring both username and email for all users.
    """

    def _create_user(
        self,
        username: str,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Dict[str, Any]
    ) -> Any:
        """
        Create and save a user with the given username, email, and password.

        This is the core user creation method used by both create_user and
        create_superuser. It enforces validation rules and properly handles
        password hashing.

        Args:
            username: Unique username for the new user
            email: Valid email address for the new user
            password: Optional password (will be hashed before storage)
            **extra_fields: Additional fields to be saved on the user model

        Returns:
            The newly created user instance

        Raises:
            ValueError: If username or email is not provided
            ValidationError: If email format is invalid
        """
        # Validate required fields
        if not username:
            raise ValueError(_("A username must be provided"))

        if not email:
            raise ValueError(_("An email address must be provided"))

        # Normalize and validate email
        email = self.normalize_email(email)
        validate_email_address(email)

        # Get the user model dynamically to avoid circular imports
        global_user_model = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        # Normalize username according to model's rules
        username = global_user_model.normalize_username(username)

        # Create user instance but don't save to DB yet
        user = self.model(username=username, email=email, **extra_fields)

        # Hash the password and save the user
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Dict[str, Any]
    ) -> Any:
        """
        Create and save a regular user with the given username, email, and
        password.

        Regular users have is_staff and is_superuser set to False by default.

        Args:
            username: Unique username for the new user
            email: Valid email address for the new user
            password: Optional password (will be hashed before storage)
            **extra_fields: Additional fields to be saved on the user model

        Returns:
            The newly created regular user instance
        """
        # Set default permissions for regular users
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Dict[str, Any]
    ) -> Any:
        """
        Create and save a superuser with the given username, email, and
        password.

        Superusers have both is_staff and is_superuser set to True.

        Args:
            username: Unique username for the new superuser
            email: Valid email address for the new superuser
            password: Optional password (will be hashed before storage)
            **extra_fields: Additional fields to be saved on the user model

        Returns:
            The newly created superuser instance

        Raises:
            ValueError: If is_staff or is_superuser is explicitly set to False
        """
        # Set default permissions for superusers
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Validate superuser permissions
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(username, email, password, **extra_fields)
