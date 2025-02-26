from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm

# Get the custom User model defined in the project
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.

    Extends Django's BaseUserAdmin to provide a tailored admin interface
    for the custom User model with appropriate forms, display fields,
    and fieldsets.
    """

    # Custom forms for creating and changing users
    form = UserChangeForm
    add_form = UserCreationForm

    # Fields to display in the user list view
    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_superuser",
    ]

    # Fields that link to the change page when clicked
    list_display_links = ["pkid", "id", "email", "username"]

    # Fields available for searching users
    search_fields = ["email", "first_name", "last_name"]

    # Default ordering in the admin list view
    ordering = ["pkid"]

    # Field groupings for the user detail view
    fieldsets = (
        # Login credentials section
        (_("Login Credentials"), {"fields": ("email", "password")}),
        # Personal information section
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "username")},
        ),
        # Permissions and group memberships section
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        # Important dates section (auto-populated)
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Field groupings for the add user form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
