from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category


class CategoryAdmin(DjangoMpttAdmin):
    """
    Admin interface configuration for the Category model.
    Inherits from DjangoMpttAdmin to provide hierarchical category management.
    """

    # Fields to display in the admin list view
    list_display = ["name", "slug", "parent", "is_active"]

    # Fields that can be filtered in the right sidebar
    list_filter = ["is_active"]

    # Fields that can be edited directly from the list view
    list_editable = ["is_active"]

    # Automatically populate the slug field based on the name
    prepopulated_fields = {"slug": ("name",)}

    # Fields that can be searched in the admin search bar
    search_fields = [
        "name",  # Search by category name
        "slug",  # Search by category slug
    ]


# Register the Category model with its custom admin configuration
admin.site.register(Category, CategoryAdmin)
