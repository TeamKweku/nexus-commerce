from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

# Get the custom User model defined in the project
User = get_user_model()


class UserChangeForm(BaseUserChangeForm):
    """
    Form for updating user data in the admin interface.

    Extends Django's BaseUserChangeForm to work with the custom User model.
    This form is used for editing existing users and their attributes.

    Attributes:
        Meta: Inner class defining the model and fields to be included in
        the form
    """

    class Meta(BaseUserChangeForm.Meta):
        """
        Metadata class for UserChangeForm.

        Specifies the User model and which fields should be editable in
        the form.
        """

        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserCreationForm(admin_forms.UserCreationForm):
    """
    Form for creating new users in the admin interface.

    Extends Django's UserCreationForm to work with the custom User model.
    Adds custom validation to prevent duplicate usernames and emails.

    Attributes:
        Meta: Inner class defining the model and fields to be included in
        the form error_messages: Dictionary of custom error messages for
        validation failures
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        """
        Metadata class for UserCreationForm.

        Specifies the User model and which fields should be included when
        creating a new user through this form.
        """

        model = User
        fields = ["first_name", "last_name", "username", "email"]

    # Custom error messages for validation failures
    error_messages = {
        "duplicate_username": "Username already exists.",
        "duplicate_email": "Email already exists.",
    }

    def clean_email(self) -> str:
        """
        Validate that the email is unique across all users.

        This method is called during form validation to ensure the provided
        email address is not already in use by another user.

        Returns:
            str: The validated email address

        Raises:
            ValidationError: If the email is already associated with an
            existing user
        """
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email

    def clean_username(self) -> str:
        """
        Validate that the username is unique across all users.

        This method is called during form validation to ensure the provided
        username is not already in use by another user.

        Returns:
            str: The validated username

        Raises:
            ValidationError: If the username is already associated with an
            existing user
        """
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages["duplicate_username"]
            )
        return username
