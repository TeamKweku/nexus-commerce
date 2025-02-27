# Import necessary modules
import logging
from typing import Optional

from django.conf import settings
from djoser.social.views import ProviderAuthView
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
    """
    Custom view for obtaining JWT token pair (access and refresh tokens).
    Extends the default TokenObtainPairView to add cookie-based token storage.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Call parent class's post method to generate tokens
        token_res = super().post(request, *args, **kwargs)

        # If token generation was successful
        if token_res.status_code == status.HTTP_200_OK:
            # Extract tokens from response data
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            # If both tokens are present
            if access_token and refresh_token:
                # Set authentication cookies
                set_auth_cookies(
                    token_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Remove tokens from response data for security
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)

                # Add success message
                token_res.data["message"] = "Login Successful."
            else:
                # Handle missing tokens
                token_res.data["message"] = "Login Failed"
                logger.error(
                    "Access or refresh token not found in login response data"
                )

        return token_res


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT access tokens.
    Extends the default TokenRefreshView to handle cookie-based token storage.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Get refresh token from cookies
        refresh_token = request.COOKIES.get("refresh")

        # If refresh token exists in cookies, add it to request data
        if refresh_token:
            request.data["refresh"] = refresh_token

        # Call parent class's post method to refresh tokens
        refresh_res = super().post(request, *args, **kwargs)

        # If token refresh was successful
        if refresh_res.status_code == status.HTTP_200_OK:
            # Extract new access token from response
            access_token = refresh_res.data.get("access")

            # If both tokens are present
            if access_token and refresh_token:
                # Set new authentication cookies
                set_auth_cookies(
                    refresh_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Remove tokens from response data for security
                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                # Add success message
                refresh_res.data["message"] = (
                    "Access tokens refreshed successfully"
                )
            else:
                # Handle missing tokens
                refresh_res.data["message"] = (
                    "Access or refresh tokens not found inrefresh response data"
                )
                logger.error(
                    "Access or refresh token not found in refresh response data"
                )

        return refresh_res


class CustomProviderAuthView(ProviderAuthView):
    """
    Custom view for handling social authentication provider responses.
    Extends ProviderAuthView to add cookie-based token storage for social auth.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Call parent class's post method to handle provider authentication
        provider_res = super().post(request, *args, **kwargs)

        # If user was successfully created/authenticated
        if provider_res.status_code == status.HTTP_201_CREATED:
            # Extract tokens from provider response
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            # If both tokens are present
            if access_token and refresh_token:
                # Set authentication cookies
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Remove tokens from response data for security
                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                # Add success message
                provider_res.data["message"] = "You are logged in Successful."
            else:
                # Handle missing tokens
                provider_res.data["message"] = (
                    "Access or refresh token not found in provider response"
                )
                logger.error(
                    "Access or refresh token not found in provider res data"
                )

        return provider_res


class LogoutAPIView(APIView):
    """
    View for handling user logout.
    Clears all authentication-related cookies.
    """

    def post(self, request: Request, *args, **kwargs):
        # Create empty response with success status
        response = Response(status=status.HTTP_204_NO_CONTENT)
        # Delete all authentication cookies
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
