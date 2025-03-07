from typing import List, Type

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models

from .models import ContentView


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    """
    Admin configuration for ContentView model.
    Displays key information about content views in the Django admin interface.

    Attributes:
        list_display: Fields to display in the list view, showing content
        object, viewer details, and timestamp
    """

    list_display: List[str] = [
        "content_object",  # The object that was viewed
        "user",  # User who viewed the content
        "viewer_ip",  # IP address of the viewer
        "created_at",  # When the view was recorded
    ]


class ContentViewInline(GenericTabularInline):
    """
    Inline admin configuration for ContentView model.
    Allows viewing content views directly in the admin page of related models.

    This inline can be included in any model's admin to show its view
    statistics. Uses Django's GenericTabularInline for generic relation
    support.

    Attributes:
        model: The model class to be displayed inline
        extra: Number of extra empty forms to display
        readonly_fields: Fields that cannot be modified through the
        inline interface
    """

    model: Type[models.Model] = ContentView  # The model to be displayed inline
    extra: int = 0  # No extra empty forms

    readonly_fields: List[str] = [
        "user",  # Who viewed the content
        "viewer_ip",  # Their IP address
        "created_at",  # When the view occurred
    ]
