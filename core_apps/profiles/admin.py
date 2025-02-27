from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    Customizes how Profile objects are displayed and managed in Django admin.
    """

    # Fields to display in the list view
    list_display = [
        "pkid",
        "id",
        "user",
        "user_type",
        "phone_number",
        "billing_country",
    ]

    # Fields that link to the detail view
    list_display_links = ["pkid", "id", "user"]

    # Fields available for filtering in the right sidebar
    list_filter = ["user_type"]

    # Fields that can be searched in the admin search bar
    search_fields = [
        "user__username",  # Search by username
        "user__email",  # Search by email
        "billing_city",  # Search by billing city
        "shipping_city",  # Search by shipping city
    ]

    # Number of items to display per page
    list_per_page = 25
