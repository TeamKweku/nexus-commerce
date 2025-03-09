from typing import List

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    Customizes how Profile objects are displayed and managed in Django admin.

    Attributes:
        list_display (List[str]): Fields to display in the list view
        list_display_links (List[str]): Fields that link to the detail view
        list_filter (List[str]): Fields available for filtering in the right
          sidebar
        search_fields (List[str]): Fields that can be searched in the admin
          search bar
        list_per_page (int): Number of items to display per page
    """

    list_display: List[str] = [
        "pkid",
        "id",
        "user",
        "user_type",
        "phone_number",
        "country",
    ]

    list_display_links: List[str] = ["pkid", "id", "user"]

    list_filter: List[str] = ["user_type"]

    search_fields: List[str] = [
        "user__username",  # Search by username
        "user__email",  # Search by email
        "city",  # Search by city
    ]

    list_per_page: int = 25
