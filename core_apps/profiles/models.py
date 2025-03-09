from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel

# Get the active User model as defined in settings
User = get_user_model()


def get_user_username(instance: "Profile") -> str:
    """
    Generate username for profile slug creation.

    Args:
        instance: Profile instance being processed

    Returns:
        str: Username associated with the profile
    """
    return instance.user.username


class Profile(TimeStampedModel):
    """
    User profile model storing additional user information.

    Inherits from TimeStampedModel to include creation and update timestamps.
    Links to User model in a one-to-one relationship.

    Attributes:
        user: One-to-one relationship with User model
        user_type: Role-based user categorization
        avatar: User's profile picture stored in Cloudinary
        bio: User's biographical information
        phone_number: Contact number in international format
        address: User's physical address
        country: User's country of residence
        city: User's city of residence
        slug: URL-friendly unique identifier
    """

    class UserType(models.TextChoices):
        """
        Enumeration of available user types.

        Attributes:
            BUYER: Regular customer role
            SELLER: Merchant role
            ADMIN: Administrative role
        """

        BUYER = "buyer", _("Buyer")
        SELLER = "seller", _("Seller")
        ADMIN = "admin", _("Admin")

    user: models.OneToOneField = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_type: models.CharField = models.CharField(
        verbose_name=_("User Type"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.BUYER,
    )
    avatar: CloudinaryField = CloudinaryField(
        verbose_name=_("Avatar"), blank=True, null=True
    )
    bio: models.TextField = models.TextField(
        verbose_name=_("Bio"), blank=True, null=True
    )
    phone_number: PhoneNumberField = PhoneNumberField(
        verbose_name=_("Phone Number"),
        max_length=30,
        blank=True,
        help_text=_(
            "Enter phone number in international format (e.g., +233123456789)"
        ),
    )
    address: models.CharField = models.CharField(
        verbose_name=_("Address"),
        max_length=255,
        blank=True,
        null=True,
    )
    country: CountryField = CountryField(
        verbose_name=_("Country"), default="GH"
    )
    city: models.CharField = models.CharField(
        verbose_name=_("City"), max_length=180, default="Accra"
    )
    slug: AutoSlugField = AutoSlugField(
        populate_from=get_user_username, unique=True
    )

    def __str__(self) -> str:
        """
        Generate string representation of Profile.

        Returns:
            str: Profile identifier using username
        """
        return f"{self.user.username}'s Profile"

    class Meta:
        """
        Model metadata options.
        """

        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
