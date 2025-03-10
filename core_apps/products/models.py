from decimal import Decimal

from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey

from core_apps.categories.models import Category
from core_apps.common.models import TimeStampedModel

from .fields import OrderField


class Attribute(TimeStampedModel):
    """
    Model for product attributes (e.g., Color, Size, Material).

    Attributes:
        name: Unique identifier for the attribute
        description: Optional detailed description of the attribute
    """

    name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
    )
    description: models.TextField = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class AttributeValue(TimeStampedModel):
    """
    Model for specific values of attributes (e.g., Red, XL, Cotton).

    Attributes:
        attribute_value: Specific value for an attribute
        attribute: Reference to the parent attribute
    """

    attribute_value: models.CharField = models.CharField(max_length=100)
    attribute: models.ForeignKey = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="attribute_value",
    )

    def __str__(self) -> str:
        return f"{self.attribute.name}-{self.attribute_value}"


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
    """
    Custom queryset to filter active products.

    Provides methods to filter objects based on their active status.
    """

    def is_active(self) -> models.QuerySet:
        """Filter queryset to return only active items."""
        return self.filter(is_active=True)


class Product(TimeStampedModel):
    """
    Core Product model representing basic product information.

    This model stores the fundamental details of a product, serving as the base
    for more specific product variations (ProductLine).

    Attributes:
        name: Product's display name
        slug: URL-friendly identifier
        description: Detailed product description
        is_digital: Whether the product is digital or physical
        category: Product's category in the hierarchy
        is_active: Product's visibility status
        attribute_values: Associated attribute values
        product_type: Type classification of the product
    """

    name: models.CharField = models.CharField(
        verbose_name=_("Product Name"),
        max_length=100,
        help_text=_("Format: required, max-length=100"),
    )
    slug: AutoSlugField = AutoSlugField(
        populate_from=get_product_slug,
        unique=True,
    )
    description: models.TextField = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("Format: optional"),
    )
    is_digital: models.BooleanField = models.BooleanField(
        verbose_name=_("Digital Product"),
        default=False,
        help_text=_("Format: true=Digital Product, false=Physical Product"),
    )
    category: TreeForeignKey = TreeForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Category"),
    )
    is_active: models.BooleanField = models.BooleanField(default=False)
    attribute_values: models.ManyToManyField = models.ManyToManyField(
        "AttributeValue",
        through="ProductAttributeValue",
        related_name="product_attr_value",
        verbose_name=_("Product Attributes"),
    )
    product_type: models.ForeignKey = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_type"
    )

    objects: Manager = IsActiveQueryset.as_manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


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
    product_type = models.ForeignKey(
        "ProductType",
        on_delete=models.PROTECT,
        related_name="product_line_type",
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    weight = models.FloatField()
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)
    attribute_value = models.ManyToManyField(
        "AttributeValue",
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
        verbose_name=_("Attribute Values"),
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
        if self.price is None:
            raise ValidationError(_("Price is required."))

        if self.price <= 0:
            raise ValidationError(_("Price must be greater than zero."))

        if self.stock_qty is None:
            raise ValidationError(_("Stock quantity is required."))

        if self.stock_qty < 0:
            raise ValidationError(_("Stock quantity cannot be negative."))

        if self.weight is None:
            raise ValidationError(_("Weight is required."))

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


class ProductAttributeValue(TimeStampedModel):
    """
    Bridge model linking Product with AttributeValue.
    Defines which attribute values are available at product level.
    """

    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_value_av",
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="product_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product")


class ProductLineAttributeValue(TimeStampedModel):
    """
    Bridge model linking ProductLine with AttributeValue.
    Defines specific attribute values for each product variant.
    """

    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product_line = models.ForeignKey(
        "ProductLine",
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")

    def clean(self):
        """
        Validate that no duplicate attributes exist for a product line.
        """
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value
            )
            .filter(product_line=self.product_line)
            .exists()
        )

        if not qs:
            iqs = Attribute.objects.filter(
                attribute_value__product_attribute_value_av=self.product_line
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError(_("Duplicate attribute exists"))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductType(TimeStampedModel):
    """
    ProductType model defining categories of products with shared attributes.
    Example: T-Shirt, Book, Digital Download
    """

    name = models.CharField(
        verbose_name=_("Type Name"),
        max_length=100,
        unique=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    attribute = models.ManyToManyField(
        Attribute,
        through="ProductTypeAttribute",
        related_name="product_type_attribute",
    )

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")
        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class ProductTypeAttribute(TimeStampedModel):
    """
    Bridge model linking ProductType with Attribute.
    Defines which attributes are available for products of this type.
    """

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_at",
    )

    class Meta:
        unique_together = ("product_type", "attribute")
        verbose_name = _("Product Type Attribute")
        verbose_name_plural = _("Product Type Attributes")
