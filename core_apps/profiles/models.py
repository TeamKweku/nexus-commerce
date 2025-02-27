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
    Helper function to get username for slug generation.

    Args:
        instance: Profile instance being processed

    Returns:
        str: Username associated with the profile
    """
    return instance.user.username


class Profile(TimeStampedModel):
    """
    User profile model storing additional user information.

    Extends TimeStampedModel to include creation and update timestamps.
    Links to User model in a one-to-one relationship.
    """

    class UserType(models.TextChoices):
        """
        Enumeration of available user types.
        Provides role-based distinction between different user categories.
        """

        BUYER = "buyer", _("Buyer")
        SELLER = "seller", _("Seller")
        ADMIN = "admin", _("Admin")

    # Core Fields
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  # Delete profile when user is deleted
        related_name="profile",
    )
    user_type = models.CharField(
        verbose_name=_("User Type"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.BUYER,
    )

    # Profile Information
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)
    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+23324874633"
    )

    # Billing Information
    billing_address = models.CharField(
        verbose_name=_("Billing Address"), max_length=255, blank=True, null=True
    )
    billing_country = CountryField(
        verbose_name=_("Billing Country"), default="GH"
    )
    billing_city = models.CharField(
        verbose_name=_("Billing City"), max_length=180, default="Accra"
    )

    # Shipping Information
    shipping_address = models.CharField(
        verbose_name=_("Shipping Address"),
        max_length=255,
        blank=True,
        null=True,
    )
    shipping_country = CountryField(
        verbose_name=_("Shipping Country"), default="GH"
    )
    shipping_city = models.CharField(
        verbose_name=_("Shipping City"), max_length=180, default="Accra"
    )

    # Auto-generated slug field for URLs
    slug = AutoSlugField(populate_from=get_user_username, unique=True)

    def __str__(self) -> str:
        """
        String representation of the Profile.

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
