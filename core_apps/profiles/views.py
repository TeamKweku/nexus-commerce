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
        operation_description="""
        Retrieves a paginated list of all user profiles, excluding staff and
        superusers.

        Features:
        - Pagination: Default 9 items per page
        - Search: Filter by username, first name, or last name
        - Filtering: Filter by user type, country, and city

        Example search: /api/v1/profiles/all/?search=john
        Example filter: /api/v1/profiles/all/?user_type=buyer&country=GH
        """,
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                example=1,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page (default: 9, max: 100)",
                type=openapi.TYPE_INTEGER,
                example=9,
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search profiles by username, first name, or"
                "last name",
                type=openapi.TYPE_STRING,
                example="john",
            ),
            openapi.Parameter(
                "user_type",
                openapi.IN_QUERY,
                description="Filter by user type",
                type=openapi.TYPE_STRING,
                enum=["buyer", "seller", "admin"],
                example="buyer",
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Filter by country code (ISO 3166-1 alpha-2)",
                type=openapi.TYPE_STRING,
                example="GH",
            ),
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="Filter by city name",
                type=openapi.TYPE_STRING,
                example="Accra",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successfully retrieved profiles",
                examples={
                    "application/json": {
                        "status_code": 200,
                        "message": "Successfully retrieved profiles",
                        "profiles": {
                            "count": 2,
                            "next": "http://api/v1/profiles/all/?page=2",
                            "previous": None,
                            "results": [
                                {
                                    "id": "550e8400-e29b-41d4-"
                                    "a716-446655440000",
                                    "username": "john_doe",
                                    "first_name": "John",
                                    "last_name": "Doe",
                                    "full_name": "John Doe",
                                    "user_type": "buyer",
                                    "avatar": "http://example.com/avatar.jpg",
                                    "bio": "Tech enthusiast",
                                    "phone_number": "+233123456789",
                                    "country": "Ghana",
                                    "city": "Accra",
                                    "date_joined": "2023-01-01T00:00:00Z",
                                }
                            ],
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "status_code": 400,
                        "message": "Invalid request parameters",
                        "errors": {
                            "page": ["Page number must be a positive integer."],
                            "user_type": ["Invalid user type specified."],
                        },
                    }
                },
            ),
            401: "Unauthorized - Authentication credentials were not provided",
            403: "Forbidden - You do not have permission to perform"
            "this action",
        },
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
        operation_summary="Get Current User Profile",
        operation_description="Retrieves the profile of the currently"
        "authenticated user.",
        responses={200: ProfileSerializer, 404: "Profile not found"},
        tags=["Profiles"],
    )
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

    @swagger_auto_schema(
        operation_summary="Get Profile for Update",
        operation_description="Retrieves the current user's profile for"
        "updating.",
        responses={200: UpdateProfileSerializer, 404: "Profile not found"},
        tags=["Profiles"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Profile",
        operation_description="Partially updates the authenticated user's"
        "profile.",
        request_body=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            400: "Bad Request",
            404: "Profile not found",
        },
        tags=["Profiles"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Full Update Profile",
        operation_description="Completely updates the authenticated user's"
        "profile.",
        request_body=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            400: "Bad Request",
            404: "Profile not found",
        },
        tags=["Profiles"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Upload Profile Avatar",
        operation_description="Upload a new avatar image for the user profile.",
        request_body=AvatarUploadSerializer,
        responses={
            202: openapi.Response(
                description="Avatar upload accepted",
                examples={
                    "application/json": {"message": "Avatar upload started."}
                },
            ),
            400: "Invalid image format or data",
        },
        tags=["Profiles"],
    )
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

    @swagger_auto_schema(
        operation_summary="Get Public Profile",
        operation_description="Retrieves a user's public profile information"
        "by slug.",
        responses={200: ProfileSerializer, 404: "Profile not found"},
        tags=["Profiles"],
    )
    def get_queryset(self) -> QuerySet:
        """Returns base queryset excluding staff and superusers."""
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .select_related("user")
        )
