import logging
from typing import Optional, Tuple, Union

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token

# Configure logger for authentication-related events
logger: logging.Logger = logging.getLogger(__name__)


class CookieAuthentication(JWTAuthentication):
    """
    Custom authentication class that extends JWT authentication to
    support cookies.

    This class implements a dual authentication strategy:
    1. The Authorization header (standard JWT behavior)
    2. A cookie (custom implementation)

    The authentication process follows this sequence:
    1. Check Authorization header for token
    2. If not found, check cookies for token
    3. Validate found token
    4. Return authenticated user and token

    Attributes:
        Inherits all attributes from JWTAuthentication
    """

    def authenticate(
        self, request: Request
    ) -> Optional[Tuple[AuthUser, Token]]:
        """
        Authenticate the request using JWT token from header or cookie.

        The method attempts to find a valid token in the following order:
        1. Authorization header
        2. Cookie specified by settings.COOKIE_NAME

        Args:
            request: The incoming HTTP request object containing headers
            and cookies

        Returns:
            Optional[Tuple[AuthUser, Token]]: A tuple containing the
            authenticated
                user and valid token if authentication succeeds, None if:
                - No token found in header or cookie
                - Token validation fails
                - User lookup fails

        Raises:
            No exceptions are raised; all errors are logged and None is returned
        """
        # First try to get token from Authorization header
        header: Optional[bytes] = self.get_header(request)
        raw_token: Optional[Union[str, bytes]] = None

        # Check for token in header first
        if header is not None:
            raw_token = self.get_raw_token(header)
        # If not in header, check for token in cookies
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)

        # If we found a token, try to validate it
        if raw_token is not None:
            try:
                # Validate the token and get associated user
                validated_token: Token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token

            except TokenError as e:
                # Log any token validation errors
                logger.error(f"Token validation error: {str(e)}")

        # Return None if no valid token was found
        return None
