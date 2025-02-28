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
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    """
    Set authentication cookies in the response.

    Args:
        response: The HTTP response object
        access_token: JWT access token to be stored in cookie
        refresh_token: Optional JWT refresh token to be stored in cookie
    """
    # Calculate access token expiry from settings
    access_token_lifetime = settings.SIMPLE_JWT[
        "ACCESS_TOKEN_LIFETIME"
    ].total_seconds()

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
        refresh_token_lifetime = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ].total_seconds()
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
        token_res = super().post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)

                token_res.data["message"] = "Login Successful"
            else:
                token_res.data["message"] = "Login Failed"
                logger.error(
                    "Access or refresh token not found in login response data"
                )

        return token_res


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
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")

            if access_token and refresh_token:
                set_auth_cookies(
                    refresh_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = (
                    "Access tokens refreshed successfully"
                )
            else:
                refresh_res.data["message"] = (
                    "Access or refresh tokens not found in refresh response "
                    "data"
                )
                logger.error(
                    "Access or refresh token not found in refresh response data"
                )

        return refresh_res


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
        provider_res = super().post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                provider_res.data["message"] = "You are logged in Successfully"
            else:
                provider_res.data["message"] = (
                    "Access or refresh token not found in provider response"
                )
                logger.error(
                    "Access or refresh token not found in provider response"
                    "data"
                )

        return provider_res


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
