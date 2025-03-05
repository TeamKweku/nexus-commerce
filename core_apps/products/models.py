from decimal import Decimal

from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.categories.models import Category
from core_apps.common.models import TimeStampedModel

from .fields import OrderField


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


class ProductLine(TimeStampedModel):
    """
    ProductLine model representing specific variants of a product.
    Example: Different sizes or colors of the same product.

    Inherits from TimeStampedModel to include:
    - UUID-based id
    - Auto-managed created_at and updated_at fields
    - BigAutoField pkid as primary key
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="product_lines",
        verbose_name=_("Product"),
        help_text=_("Format: required, references Product model"),
    )

    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("Format: maximum price 999.99, decimal places 2"),
    )

    sku = models.CharField(
        verbose_name=_("Stock Keeping Unit"),
        max_length=10,
        unique=True,
        help_text=_("Format: required, unique, max-length=10"),
    )

    stock_qty = models.PositiveIntegerField(
        verbose_name=_("Stock Quantity"),
        default=0,
        help_text=_("Format: required, default=0"),
    )

    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        default=False,
        help_text=_("Format: true=product line is active"),
    )

    weight = models.FloatField(
        verbose_name=_("Weight"),
        help_text=_("Format: required, in kilograms"),
    )

    order = OrderField(
        unique_for_field="product",
        blank=True,  # Allow blank, OrderField will handle assignment
        verbose_name=_("Display Order"),
        help_text=_("Format: auto-assigned if not specified"),
    )

    objects = IsActiveQueryset.as_manager()

    class Meta:
        verbose_name = _("Product Line")
        verbose_name_plural = _("Product Lines")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    def clean(self):
        """Validate product line data"""
        if self.price <= 0:
            raise ValidationError(_("Price must be greater than zero."))

        if self.stock_qty < 0:
            raise ValidationError(_("Stock quantity cannot be negative."))

        if self.weight <= 0:
            raise ValidationError(_("Weight must be greater than zero."))

        # Check for duplicate order within same product
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError(
                    _("Duplicate order value for this product.")
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductImage(TimeStampedModel):
    """
    Model for storing product line images.
    Multiple images can be associated with a single product line.
    """

    alternative_text = models.CharField(
        verbose_name=_("Alternative Text"),
        max_length=100,
        help_text=_("Format: required, max-length=100"),
    )
    url = models.ImageField(
        verbose_name=_("Image URL"),
        upload_to="product_images/",
        default="product_images/default.jpg",
        help_text=_("Format: required, default image provided"),
    )
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name=_("Product Line"),
        help_text=_("Format: required, references ProductLine"),
    )
    order = OrderField(
        unique_for_field="product_line",
        blank=True,
        verbose_name=_("Display Order"),
        help_text=_("Format: auto-assigned if not specified"),
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ["order"]

    def __str__(self):
        return f"{self.product_line.sku}_img_{self.order}"

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError(
                    _("Duplicate order value for this product line.")
                )
