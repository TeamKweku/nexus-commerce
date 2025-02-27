# Import necessary modules
import logging
from typing import Optional

from django.conf import settings
from djoser.social.views import ProviderAuthView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Configure logging for this module
logger = logging.getLogger(__name__)


def set_auth_cookies(
    response: Response,
    /,  # positional-only
    access_token: str,
    refresh_token: Optional[str] = None,
) -> None:
    """Store authentication tokens as HTTP cookies.

    :param response: Response to modify
    :param access_token: Token to store
    :param refresh_token: Optional refresh token
    """
    # Calculate access token expiry from settings
    jwt_settings = settings.SIMPLE_JWT
    access_expiry = jwt_settings["ACCESS_TOKEN_LIFETIME"]
    access_token_lifetime = access_expiry.total_seconds()

    # Base cookie settings for security and configuration
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }

    # Set access token cookie
    response.set_cookie("access", access_token, **cookie_settings)

    # If refresh token provided, set it with its own expiry time
    if refresh_token:
        refresh_expiry = jwt_settings["REFRESH_TOKEN_LIFETIME"]
        refresh_token_lifetime = refresh_expiry.total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    # Set logged_in cookie for frontend state management
    # This cookie is accessible via JavaScript
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="""
        Authenticate a user and obtain JWT tokens.       
        The tokens will be set as HTTP-only cookies for enhanced security.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User email address"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User password"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login Successful",
                        "user": {"id": "uuid4", "email": "user@example.com"},
                    }
                },
            ),
            401: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "detail": "No active account found with the given "
                        "credentials"
                    }
                },
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh Access Token",
        operation_description="""
        Obtain a new access token using refresh token.      
        The refresh token should be present in the cookies.
        A new access token will be set as an HTTP-only cookie.
        """,
        responses={
            200: openapi.Response(
                description="Token refresh successful",
                examples={
                    "application/json": {
                        "message": "Access tokens refreshed successfully"
                    }
                },
            ),
            401: openapi.Response(
                description="Invalid or expired refresh token",
                examples={
                    "application/json": {
                        "detail": "Token is invalid or expired"
                    }
                },
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class CustomProviderAuthView(ProviderAuthView):
    @swagger_auto_schema(
        operation_summary="Social Authentication",
        operation_description="""
        Authenticate using a social provider (Google, Facebook, etc.).     
        Handles the OAuth2 callback and sets JWT tokens as cookies upon 
        successful authentication.
        """,
        manual_parameters=[
            openapi.Parameter(
                "provider",
                openapi.IN_PATH,
                description="Social auth provider (e.g., 'google', 'facebook')",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="OAuth2 authorization code",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Social authentication successful",
                examples={
                    "application/json": {
                        "message": "You are logged in Successfully",
                        "user": {"id": "uuid4", "email": "user@example.com"},
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid OAuth2 code or provider",
                examples={
                    "application/json": {
                        "detail": "Invalid OAuth2 authorization code"
                    }
                },
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class LogoutAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="""
        Log out the current user.
        
        Clears all authentication cookies (access token, refresh token, and
        logged_in status).
        """,
        responses={
            204: openapi.Response(
                description="Successfully logged out",
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request: Request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
