from typing import Any, Dict, Optional

from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import parse as parse_phone
from phonenumbers.phonenumberutil import NumberParseException
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Profile information.

    Combines data from both User and Profile models for complete profile
    representation.

    Attributes:
        first_name: User's first name (read-only)
        last_name: User's last name (read-only)
        username: User's username (read-only)
        full_name: User's full name (read-only)
        date_joined: User's registration date (read-only)
        avatar: URL of user's profile picture
        phone_number: Validated phone number field
        country: Country name field
    """

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    date_joined = serializers.DateTimeField(
        source="user.date_joined", read_only=True
    )

    avatar = serializers.SerializerMethodField()
    phone_number = PhoneNumberField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "username",
            "full_name",
            "date_joined",
            "user_type",
            "avatar",
            "bio",
            "phone_number",
            "address",
            "country",
            "city",
        ]

    def get_avatar(self, obj: Profile) -> Optional[str]:
        """
        Get the URL of the profile avatar.

        Args:
            obj: Profile instance being serialized

        Returns:
            str: URL of the avatar if it exists
            None: If no avatar is set
        """
        try:
            return obj.avatar.url
        except AttributeError:
            return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Profile information.

    Handles validation and updates for both profile and related
    user model fields.

    Attributes:
        first_name: User's first name
        last_name: User's last name
        username: User's username
        phone_number: Validated phone number field
        country: Country name field
    """

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    phone_number = PhoneNumberField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "username",
            "user_type",
            "bio",
            "phone_number",
            "address",
            "country",
            "city",
        ]

    def validate_phone_number(self, value: str) -> str:
        """
        Validate phone number format based on the country specified.

        Args:
            value: Phone number string to validate

        Returns:
            str: Validated phone number

        Raises:
            serializers.ValidationError: If phone number format is invalid
        """
        try:
            country = self.initial_data.get("country") or self.instance.country
            parsed_number = parse_phone(value, country)
            if not parsed_number.is_valid():
                raise serializers.ValidationError(
                    "Invalid phone number format for the specified country."
                )
            return value
        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")

    def update(
        self, instance: Profile, validated_data: Dict[str, Any]
    ) -> Profile:
        """
        Update profile and related user instance with validated data.

        Args:
            instance: Profile instance to update
            validated_data: Dictionary of validated fields and values

        Returns:
            Profile: Updated profile instance
        """
        user_data = validated_data.pop("user", {})

        # Update User model fields
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class AvatarUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for handling avatar image uploads.
    """

    avatar = serializers.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ["avatar"]
