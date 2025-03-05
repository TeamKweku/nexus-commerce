from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Product, ProductImage, ProductLine


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            "admin:{}_{}_change".format(
                instance._meta.app_label, instance._meta.model_name
            ),
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        return ""


class ProductLineInline(EditLinkInline, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["name"]
    readonly_fields = ["slug"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["sku", "product", "price", "stock_qty", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["sku", "product__name"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product_line", "alternative_text", "order"]
    list_filter = ["product_line"]
    search_fields = ["alternative_text", "product_line__sku"]