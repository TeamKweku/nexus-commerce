from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from core_apps.common.models import TimeStampedModel


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class Category(MPTTModel, TimeStampedModel):
    """
    Category model implementing MPTT for hierarchical structure.
    Inherits from TimeStampedModel for audit fields.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        max_length=235,
        unique=True,
        help_text=_("Format: required, unique, max-length=235"),
    )
    slug = models.SlugField(
        verbose_name=_("Category Slug"),
        max_length=255,
        unique=True,
        help_text=_("Format: required, unique, max-length=255"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("Format: optional"),
    )
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent Category"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        help_text=_("Format: optional, references 'Category' model"),
    )
    is_active = models.BooleanField(
        verbose_name=_("Category Active"),
        default=False,
        help_text=_("Format: true=category visible"),
    )

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
