from typing import Any

from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from core_apps.common.models import TimeStampedModel


def get_category_slug(instance: Any) -> str:
    """
    Helper function to generate slug from category name.

    Args:
        instance: Category instance being processed

    Returns:
        str: Name to be used for slug generation
    """
    return instance.name


class CategoryManager(models.Manager):
    """
    Custom manager for Category model providing additional query methods.
    """

    def active(self) -> models.QuerySet:
        """
        Get all active categories.

        Returns:
            QuerySet: Filtered queryset containing only active categories
        """
        return self.filter(is_active=True)


class Category(MPTTModel, TimeStampedModel):
    """
    Category model implementing MPTT for hierarchical structure.
    Inherits from TimeStampedModel for audit fields.

    Attributes:
        name: Category name (required, unique)
        slug: URL-friendly identifier (auto-generated)
        description: Optional category description
        parent: Reference to parent category (optional)
        is_active: Category visibility status
        objects: Custom manager providing additional query methods
    """

    name: models.CharField = models.CharField(
        verbose_name=_("Category Name"),
        max_length=235,
        unique=True,
        help_text=_("Format: required, unique, max-length=235"),
    )
    slug: AutoSlugField = AutoSlugField(
        populate_from=get_category_slug,
        unique=True,
    )
    description: models.TextField = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("Format: optional"),
    )
    parent: TreeForeignKey = TreeForeignKey(
        "self",
        verbose_name=_("Parent Category"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        help_text=_("Format: optional, references 'Category' model"),
    )
    is_active: models.BooleanField = models.BooleanField(
        verbose_name=_("Category Active"),
        default=False,
        help_text=_("Format: true=category visible"),
    )

    objects = CategoryManager()

    class MPTTMeta:
        """Meta configuration for MPTT model."""

        order_insertion_by = ["name"]

    class Meta:
        """Meta configuration for Category model."""

        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        """
        String representation of the category.

        Returns:
            str: Category name
        """
        return self.name
