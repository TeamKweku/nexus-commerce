from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers import parse as parse_phone
from phonenumbers.phonenumberutil import NumberParseException
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Profile information.
    Combines data from both User and Profile models.
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

    def get_avatar(self, obj: Profile) -> str | None:
        """
        Get the URL of the profile avatar.
        Returns None if no avatar is set.
        """
        try:
            return obj.avatar.url
        except AttributeError:
            return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Profile information.
    Handles both profile and related user model updates.
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

    def validate_phone_number(self, value):
        """
        Validate phone number format based on the country specified.
        """
        try:
            country = self.initial_data.get("country") or self.instance.country
            parsed_number = parse_phone(str(value), country)
            if not parsed_number.is_valid():
                raise serializers.ValidationError(
                    f"Please enter a valid phone number for {country}"
                )
            return value
        except NumberParseException:
            raise serializers.ValidationError(
                "Please enter a valid international phone number "
                "(e.g., +233123456789)"
            )

    def update(self, instance, validated_data):
        """
        Handle nested updates for both Profile and User models.
        """
        user_data = validated_data.pop("user", {})

        # Update User model fields
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update Profile model fields
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
