from django.urls import path, re_path

from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
)

# Define URL patterns for authentication endpoints
urlpatterns = [
    # Social authentication endpoint
    # Uses regex pattern to capture provider name (e.g., 'google', 'facebook')
    # Example: /api/v1/auth/o/google/
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    # Login endpoint for obtaining JWT tokens
    # POST request with email/password returns access and refresh tokens
    path("login/", CustomTokenObtainPairView.as_view()),
    # Token refresh endpoint
    # POST request with refresh token returns new access token
    path("refresh/", CustomTokenRefreshView.as_view()),
    # Logout endpoint
    # POST request clears authentication cookies
    path("logout/", LogoutAPIView.as_view()),
]
