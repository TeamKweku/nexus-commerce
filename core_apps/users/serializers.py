from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    """
    Serializer for creating new user accounts.
    Extends Djoser's UserCreateSerializer to customize user creation fields.
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "first_name", "last_name", "password"]


class CustomUserSerializer(UserSerializer):
    """
    Custom serializer for user profile data.
    Combines data from both User and Profile models.
    """

    full_name = serializers.ReadOnlyField(source="get_full_name")
    slug = serializers.ReadOnlyField(source="profile.slug")
    user_type = serializers.CharField(source="profile.user_type")
    phone_number = PhoneNumberField(source="profile.phone_number")
    avatar = serializers.ImageField(source="profile.avatar")
    bio = serializers.CharField(source="profile.bio", allow_blank=True)
    address = serializers.CharField(source="profile.address", allow_blank=True)
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "date_joined",
            "slug",
            "user_type",
            "phone_number",
            "avatar",
            "bio",
            "address",
            "country",
            "city",
        ]
        read_only_fields = ["id", "email", "date_joined"]
