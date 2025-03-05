from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from core_apps.categories.views import CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")

# Djoser endpoint documentation
djoser_endpoints = [
    {
        "name": "User Registration",
        "path": "/api/v1/auth/users/",
        "method": "POST",
        "description": """
        Register a new user account.
        A verification email will be sent to the user's email address.
        """,
        "request_body": {
            "email": "string",
            "password": "string",
            "re_password": "string",
            "username": "string",
            "first_name": "string",
            "last_name": "string",
        },
        "responses": {
            201: {"description": "User account created successfully"},
            400: {"description": "Invalid input (e.g., passwords don't match)"},
        },
    },
    {
        "name": "Password Reset",
        "path": "/api/v1/auth/users/reset_password/",
        "method": "POST",
        "description": """
        Request a password reset email.
        An email with reset instructions will be sent if the email exists.
        """,
        "request_body": {"email": "string"},
        "responses": {
            204: {"description": "Password reset email sent"},
            400: {"description": "Invalid email address"},
        },
    },
    {
        "name": "Password Reset Confirmation",
        "path": "/api/v1/auth/users/reset_password_confirm/",
        "method": "POST",
        "description": """
        Confirm password reset using token from email.
        Sets new password using the token received in email.
        """,
        "request_body": {
            "uid": "string",
            "token": "string",
            "new_password": "string",
            "re_new_password": "string",
        },
        "responses": {
            204: {"description": "Password successfully reset"},
            400: {"description": "Invalid token or passwords don't match"},
        },
    },
    {
        "name": "Email Activation",
        "path": "/api/v1/auth/users/activation/",
        "method": "POST",
        "description": """
        Activate user account using email token.
        Activates the user account using the token received in email.
        """,
        "request_body": {"uid": "string", "token": "string"},
        "responses": {
            204: {"description": "Account successfully activated"},
            400: {"description": "Invalid activation token"},
        },
    },
    {
        "name": "Resend Activation Email",
        "path": "/api/v1/auth/users/resend_activation/",
        "method": "POST",
        "description": """
        Resend account activation email.
        Sends a new activation email to the specified email address.
        """,
        "request_body": {"email": "string"},
        "responses": {
            204: {"description": "Activation email resent"},
            400: {"description": "Invalid email or account already active"},
        },
    },
    {
        "name": "Set Username",
        "path": "/api/v1/auth/users/set_username/",
        "method": "POST",
        "description": "Change user's username",
        "request_body": {
            "current_password": "string",
            "new_username": "string",
            "re_new_username": "string",
        },
        "responses": {
            204: {"description": "Username successfully changed"},
            400: {"description": "Invalid input"},
        },
    },
    {
        "name": "Set Password",
        "path": "/api/v1/auth/users/set_password/",
        "method": "POST",
        "description": "Change user's password",
        "request_body": {
            "current_password": "string",
            "new_password": "string",
            "re_new_password": "string",
        },
        "responses": {
            204: {"description": "Password successfully changed"},
            400: {"description": "Invalid input"},
        },
    },
]

# Define the custom paths for the schema
custom_paths = {}
for endpoint in djoser_endpoints:
    custom_paths[endpoint["path"]] = {
        endpoint["method"].lower(): {
            "tags": ["Djoser Authentication"],
            "operation_id": endpoint["name"].lower().replace(" ", "_"),
            "description": endpoint["description"],
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                k: {"type": "string"}
                                for k in endpoint["request_body"]
                            },
                            "required": list(endpoint["request_body"].keys()),
                        }
                    }
                }
            },
            "responses": {
                str(code): {"description": desc}
                for code, desc in endpoint["responses"].items()
            },
        }
    }

# Create schema view with Djoser endpoints
schema_view = get_schema_view(
    openapi.Info(
        title="Nexus Commerce API",
        default_version="v1",
        description="""
        Nexus Commerce REST API documentation.
        ## Authentication
        This API uses JWT tokens stored in HTTP-only cookies for authentication.
        ### Available Authentication Methods:
        - Email/Password login
        - Social authentication (Google, Facebook)
        - Token refresh
        ### Security
        - All tokens are stored as HTTP-only cookies
        - CSRF protection enabled
        - Rate limiting applied
        ## Djoser Authentication Endpoints
        This API includes several authentication endpoints provided by Djoser:
        ### User Registration and Activation
        - POST /api/v1/auth/users/ - Register new user
        - POST /api/v1/auth/users/activation/ - Activate user account
        - POST /api/v1/auth/users/resend_activation/ - Resend activation email
        ### Password Management
        - POST /api/v1/auth/users/reset_password/ - Request password reset
        - POST /api/v1/auth/users/reset_password_confirm/ - Confirm password
        - POST /api/v1/auth/users/set_password/ - Change password
        ### Account Management
        - POST /api/v1/auth/users/set_username/ - Change username
        """,
        terms_of_service="https://www.nexuscommerce.com/terms/",
        contact=openapi.Contact(email="djangotuts2022@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        path("api/v1/auth/", include("djoser.urls")),
        path("api/v1/auth/", include("core_apps.users.urls")),
        path("api/v1/profiles/", include("core_apps.profiles.urls")),
        path("api/v1/", include((router.urls, "categories"), namespace="v1")),
    ],
)

# Update the schema with custom paths
if schema_view.schema:
    schema_view.schema._paths.update(custom_paths)

urlpatterns = [
    # API documentation endpoints
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # Django admin site
    path(settings.ADMIN_URL, admin.site.urls),
    # Djoser's built-in authentication URLs (registration, password reset, etc.)
    path("api/v1/auth/", include("djoser.urls")),
    # custom authentication URLs (login, logout, token refresh, social auth)
    path("api/v1/auth/", include("core_apps.users.urls")),
    # Add this line to include profile URLs
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/", include((router.urls, "categories"), namespace="v1")),
]


admin.site.site_header = "Nexus Commerce Admin"
admin.site.site_title = "Nexus Commerce Admin Portal"
admin.site.index_title = "Welcome to Nexus Commerce Admin Portal"
