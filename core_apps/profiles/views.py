from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.common.renderers import GenericJSONRenderer

from .models import Profile
from .serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from .tasks import upload_avatar_to_cloudinary

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination settings for profile listings.
    """

    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100


class ProfileListAPIView(generics.ListAPIView):
    """
    API view to list all user profiles with filtering and search capabilities.
    Excludes staff and superuser profiles.
    """

    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    object_label = "profiles"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_fields = ["user_type", "country", "city"]

    def get_queryset(self) -> List[Profile]:
        """
        Returns queryset of regular user profiles, excluding staff and
        superusers.
        """
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .select_related("user")
            .all()
        )


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve a single profile.
    Returns the profile of the currently authenticated user.
    """

    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    def get_queryset(self) -> QuerySet:
        """
        Returns base queryset with related user data.
        """
        return Profile.objects.select_related("user").all()

    def get_object(self) -> Profile:
        """
        Retrieves the profile for the current user.
        Raises 404 if profile doesn't exist.
        """
        try:
            return Profile.objects.select_related("user").get(
                user=self.request.user
            )
        except Profile.DoesNotExist:
            raise Http404("Profile not found")


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API view to update user profile information.
    Handles both profile and related user model updates.
    """

    serializer_class = UpdateProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    def get_queryset(self):
        """
        Empty queryset since we're using get_object.
        """
        return Profile.objects.none()

    def get_object(self) -> Profile:
        """
        Gets or creates a profile for the current user.
        """
        profile, _ = Profile.objects.select_related("user").get_or_create(
            user=self.request.user
        )
        return profile

    def perform_update(self, serializer: UpdateProfileSerializer) -> Profile:
        """
        Updates both profile and user model data.
        """
        user_data = serializer.validated_data.pop("user", {})
        profile = serializer.save()
        User.objects.filter(id=self.request.user.id).update(**user_data)
        return profile


class AvatarUploadView(APIView):
    """
    API view for handling profile avatar uploads.
    Processes the upload asynchronously using Cloudinary.
    """

    renderer_classes = [GenericJSONRenderer]

    def patch(self, request, *args, **kwargs):
        """
        Handles PATCH requests for avatar uploads.
        """
        return self.upload_avatar(request, *args, **kwargs)

    def upload_avatar(self, request, *args, **kwargs):
        """
        Processes the avatar upload and queues it for Cloudinary processing.
        """
        profile = request.user.profile
        serializer = AvatarUploadSerializer(profile, data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data["avatar"]
            image_content = image.read()

            # Queue the avatar upload task
            upload_avatar_to_cloudinary.delay(str(profile.id), image_content)

            return Response(
                {"message": "Avatar upload started."},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicProfileDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve any user's public profile by slug.
    """

    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet:
        """Returns base queryset excluding staff and superusers."""
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .select_related("user")
        )
