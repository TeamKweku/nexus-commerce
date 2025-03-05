from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core_apps.common.renderers import GenericJSONRenderer
from .models import Profile
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    AvatarUploadSerializer,
)
from .tasks import upload_avatar_to_cloudinary


class ProfileViewSet(viewsets.ModelViewSet):
    renderer_classes = [GenericJSONRenderer]
    object_label = "profiles"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_fields = ["user_type", "country", "city"]
    lookup_field = "slug"

    def get_queryset(self):
        if self.action in ['my_profile', 'update_profile', 'upload_avatar']:
            return Profile.objects.select_related("user").all()
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .select_related("user")
            .all()
        )

    def get_serializer_class(self):
        if self.action == 'update_profile':
            return UpdateProfileSerializer
        if self.action == 'upload_avatar':
            return AvatarUploadSerializer
        return ProfileSerializer

    @swagger_auto_schema(
        operation_summary="List All Profiles",
        operation_description="Retrieves a paginated list of all user profiles, excluding staff and superusers.",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search profiles by username, first name, or last name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "user_type",
                openapi.IN_QUERY,
                description="Filter by user type",
                type=openapi.TYPE_STRING,
                enum=["buyer", "seller", "admin"],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Public Profile",
        operation_description="Retrieves a user's public profile information by slug."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get Current User Profile",
        operation_description="Retrieves the profile of the currently authenticated user."
    )
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='put',
        operation_summary="Full Update Current User Profile",
        operation_description="Fully updates the authenticated user's profile.",
        request_body=UpdateProfileSerializer
    )
    @swagger_auto_schema(
        method='patch',
        operation_summary="Partial Update Current User Profile",
        operation_description="Partially updates the authenticated user's profile.",
        request_body=UpdateProfileSerializer
    )
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='patch',
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
            400: openapi.Response(
                description="Invalid request",
                examples={
                    "application/json": {"error": "Invalid image data"}
                },
            ),
        }
    )
    @action(detail=False, methods=['patch'])
    def upload_avatar(self, request):
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile, data=request.data)

            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            image = request.FILES.get('avatar')
            if not image:
                return Response(
                    {"error": "No image file provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            image_content = image.read()
            upload_avatar_to_cloudinary.delay(str(profile.id), image_content)
            
            return Response(
                {"message": "Avatar upload started."},
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_summary="Create Profile",
        operation_description="Creates a new user profile. Note: Profiles are typically created automatically when users register.",
        request_body=ProfileSerializer,
        responses={
            201: openapi.Response(
                description="Profile created successfully",
                schema=ProfileSerializer
            ),
            400: openapi.Response(
                description="Invalid data",
                examples={
                    "application/json": {
                        "error": "Invalid profile data"
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Full Update Profile",
        operation_description="Completely updates a profile identified by its slug.",
        request_body=UpdateProfileSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=ProfileSerializer
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {
                        "error": "Profile not found"
                    }
                }
            )
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Profile",
        operation_description="Partially updates a profile identified by its slug. Only provided fields will be updated.",
        request_body=UpdateProfileSerializer,
        responses={
            200: openapi.Response(
                description="Profile partially updated successfully",
                schema=ProfileSerializer
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {
                        "error": "Profile not found"
                    }
                }
            )
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Profile",
        operation_description="Deletes a profile identified by its slug.",
        responses={
            204: openapi.Response(
                description="Profile deleted successfully"
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {
                        "error": "Profile not found"
                    }
                }
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


