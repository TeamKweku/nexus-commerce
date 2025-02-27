from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ContentView


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    """
    Admin configuration for ContentView model.
    Displays key information about content views in the Django admin interface.
    """

    # Configure which fields to display in the list view
    list_display = [
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
    """

    model = ContentView  # The model to be displayed inline
    extra = 0  # No extra empty forms

    # Fields that cannot be modified through the inline interface
    readonly_fields = [
        "user",  # Who viewed the content
        "viewer_ip",  # Their IP address
        "created_at",  # When the view occurred
    ]
