from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category


class CategoryAdmin(DjangoMpttAdmin):
    """Admin interface configuration for the Category model."""

    list_display = ["name", "slug", "parent", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    search_fields = ["name", "slug"]


admin.site.register(Category, CategoryAdmin)
