from django.contrib import admin
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


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_"
            f"{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe(f'<a href="{url}">edit</a>')
            return link
        return ""


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


class ProductLineAttributeValueInline(admin.TabularInline):
    model = ProductLineAttributeValue
    extra = 1


class AttributeValueProductInline(admin.TabularInline):
    model = AttributeValue.product_attr_value.through


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInline,
    ]


admin.site.register(ProductType, ProductTypeAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline, AttributeValueProductInline]
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["name"]
    readonly_fields = ["slug"]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductLineAttributeValueInline]
    list_display = ["sku", "product", "price", "stock_qty", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["sku", "product__name"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product_line", "alternative_text", "order"]
    list_filter = ["product_line"]
    search_fields = ["alternative_text", "product_line__sku"]
