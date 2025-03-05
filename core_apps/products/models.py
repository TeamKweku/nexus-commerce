from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.categories.models import Category
from core_apps.common.models import TimeStampedModel


def get_product_slug(instance: "Product") -> str:
    """
    Helper function to generate slug from product name.

    Args:
        instance: Product instance being processed

    Returns:
        str: Name to be used for slug generation
    """
    return instance.name


class IsActiveQueryset(models.QuerySet):
    """Custom queryset to filter active products"""

    def is_active(self):
        return self.filter(is_active=True)


class Product(TimeStampedModel):
    """
    Core Product model representing basic product information.
    Additional features like product lines, attributes will be added later.

    Inherits from TimeStampedModel to include:
    - UUID-based id
    - Auto-managed created_at and updated_at fields
    - BigAutoField pkid as primary key
    """

    name = models.CharField(
        verbose_name=_("Product Name"),
        max_length=100,
        help_text=_("Format: required, max-length=100"),
    )
    slug = AutoSlugField(
        populate_from=get_product_slug,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("Format: optional"),
    )
    is_digital = models.BooleanField(
        verbose_name=_("Digital Product"),
        default=False,
        help_text=_("Format: true=Digital Product, false=Physical Product"),
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("Product Category"),
        on_delete=models.PROTECT,
        help_text=_("Format: required, reference to Category"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        default=False,
        help_text=_("Format: true=product visible"),
    )

    objects = IsActiveQueryset.as_manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def clean(self):
        if hasattr(self, "pid") and len(self.pid) > 10:
            raise ValidationError(_("PID length cannot exceed 10 characters."))
