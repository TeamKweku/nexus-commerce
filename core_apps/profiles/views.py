from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary="List All Profiles",
        operation_description="Retrieves a paginated list of all user profiles,"
        "excluding staff and superusers.",
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page (max 100)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search profiles by username, first name, or"
                "last name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "user_type",
                openapi.IN_QUERY,
                description="Filter by user type",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Filter by country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="Filter by city",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: ProfileSerializer(many=True), 400: "Bad Request"},
        tags=["Profiles"],
    )
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

    @swagger_auto_schema(
        operation_summary="Get Profile Details",
        operation_description="Retrieves details of a specific user profile.",
        responses={200: ProfileSerializer, 404: "Profile not found"},
        tags=["Profiles"],
    )
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.select_related("user").get(user=user)
        return profile


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API view to update user profile information.
    Handles both profile and related user model updates.
    """

    serializer_class = UpdateProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    @swagger_auto_schema(
        operation_summary="Get Profile Details",
        operation_description="Retrieves the profile details of the "
        "authenticated user.",
        responses={200: UpdateProfileSerializer, 404: "Profile not found"},
        tags=["Profile"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Profile",
        operation_description="Updates the profile information of the "
        "authenticated user.",
        request_body=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            400: "Bad Request",
            404: "Profile not found",
        },
        tags=["Profile"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Replace Profile",
        operation_description="Completely replaces the profile information of "
        "the authenticated user.",
        request_body=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            400: "Bad Request",
            404: "Profile not found",
        },
        tags=["Profile"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_object(self):
        profile = Profile.objects.select_related("user").get(
            user=self.request.user
        )
        return profile


class AvatarUploadView(APIView):
    """
    API view for handling profile avatar uploads.
    Processes the upload asynchronously using Cloudinary.
    """

    renderer_classes = [GenericJSONRenderer]
    serializer_class = AvatarUploadSerializer

    @swagger_auto_schema(
        operation_summary="Upload Profile Avatar",
        operation_description="Uploads and processes a new avatar image for the"
        "user profile.",
        request_body=AvatarUploadSerializer,
        responses={
            202: openapi.Response(
                description="Avatar upload accepted",
                examples={
                    "application/json": {"message": "Avatar upload in progress"}
                },
            ),
            400: "Invalid image format or data",
            404: "Profile not found",
        },
        tags=["Profile"],
    )
    def patch(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            raise Http404("Profile not found")

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            avatar = serializer.validated_data["avatar"]
            upload_avatar_to_cloudinary.delay(profile.id, avatar)
            return Response(
                {"message": "Avatar upload in progress"},
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

    @swagger_auto_schema(
        operation_summary="Get Public Profile",
        operation_description="Retrieves the public profile of a user by slug.",
        responses={200: ProfileSerializer, 404: "Profile not found"},
        tags=["Profile"],
    )
    def get_queryset(self) -> QuerySet:
        """Returns base queryset excluding staff and superusers."""
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .select_related("user")
        )
