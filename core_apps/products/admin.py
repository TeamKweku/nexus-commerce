from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Product model"""

    list_display = ["name", "category", "is_active", "created_at"]
    list_filter = ["is_active", "is_digital", "category"]
    search_fields = ["name", "description"]
    list_editable = ["is_active"]
    list_per_page = 25
    date_hierarchy = "created_at"
    fields = [
        "name",
        "description",
        "is_digital",
        "category",
        "is_active",
    ]
