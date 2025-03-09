from typing import List, Tuple

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category


class CategoryAdmin(DjangoMpttAdmin):
    """
    Admin interface configuration for the Category model.
    Extends DjangoMpttAdmin to provide hierarchical category management.

    Attributes:
        list_display: Fields to display in the list view
        list_filter: Fields available for filtering
        list_editable: Fields that can be edited from the list view
        search_fields: Fields that can be searched
    """

    list_display: List[str] = ["name", "slug", "parent", "is_active"]
    list_filter: List[str] = ["is_active"]
    list_editable: List[str] = ["is_active"]
    search_fields: Tuple[str, ...] = ("name", "slug")


# Register the Category model with its custom admin interface
admin.site.register(Category, CategoryAdmin)
