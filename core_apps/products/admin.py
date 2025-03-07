from typing import List, Tuple, Type

from django.contrib import admin
from django.db.models import Model
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Attribute,
    AttributeValue,
    Product,
    ProductImage,
    ProductLine,
    ProductLineAttributeValue,
    ProductType,
)


class EditLinkInline:
    """Base class providing an edit link for inline model instances."""

    def edit(self, instance: Model) -> str:
        """
        Generate an HTML edit link for the given model instance.

        Args:
            instance: The model instance to create an edit link for

        Returns:
            str: HTML link to edit the instance or empty string if
            instance has no pk
        """
        url: str = reverse(
            f"admin:{instance._meta.app_label}_"
            f"{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            return mark_safe(f'<a href="{url}">edit</a>')
        return ""


class ProductLineInline(EditLinkInline, admin.TabularInline):
    """Inline admin interface for ProductLine model."""

    model: Type[ProductLine] = ProductLine
    readonly_fields: Tuple[str, ...] = ("edit",)
    extra: int = 0


class ProductImageInline(admin.TabularInline):
    """Inline admin interface for ProductImage model."""

    model: Type[ProductImage] = ProductImage
    extra: int = 1


class AttributeValueInline(admin.TabularInline):
    """Inline admin interface for AttributeValue model."""

    model: Type[AttributeValue] = AttributeValue
    extra: int = 1


class ProductLineAttributeValueInline(admin.TabularInline):
    """Inline admin interface for ProductLineAttributeValue model."""

    model: Type[ProductLineAttributeValue] = ProductLineAttributeValue
    extra: int = 1


class AttributeValueProductInline(admin.TabularInline):
    """Inline admin interface for AttributeValue through model."""

    model = AttributeValue.product_attr_value.through


class AttributeInline(admin.TabularInline):
    """Inline admin interface for Attribute through model."""

    model = Attribute.product_type_attribute.through


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """Admin interface for ProductType model."""

    inlines: List[Type[admin.TabularInline]] = [AttributeInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.

    Provides functionality for managing products including their
    product lines and attribute values.
    """

    inlines: List[Type[admin.TabularInline]] = [
        ProductLineInline,
        AttributeValueProductInline,
    ]
    list_display: List[str] = ["name", "is_active", "created_at"]
    list_filter: List[str] = ["is_active", "category"]
    search_fields: List[str] = ["name"]
    readonly_fields: List[str] = ["slug"]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    """Admin interface for Attribute model."""

    inlines: List[Type[admin.TabularInline]] = [AttributeValueInline]
    list_display: List[str] = ["name"]
    search_fields: List[str] = ["name"]


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    """
    Admin interface for ProductLine model.

    Provides functionality for managing product variants including
    their images and attribute values.
    """

    inlines: List[Type[admin.TabularInline]] = [
        ProductImageInline,
        ProductLineAttributeValueInline,
    ]
    list_display: List[str] = [
        "sku",
        "product",
        "price",
        "stock_qty",
        "is_active",
    ]
    list_filter: List[str] = ["is_active"]
    search_fields: List[str] = ["sku", "product__name"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for ProductImage model."""

    list_display: List[str] = ["product_line", "alternative_text", "order"]
    list_filter: List[str] = ["product_line"]
    search_fields: List[str] = ["alternative_text", "product_line__sku"]
