from typing import List

from django.urls import include, path
from django.urls.resolvers import URLPattern
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet

# Application namespace for URL reversing
app_name: str = "profiles"

# Initialize the DefaultRouter for RESTful endpoints
router: DefaultRouter = DefaultRouter()

# Register the ProfileViewSet with an empty prefix
# This creates the following URL patterns:
# - GET/POST /api/v1/profiles/
# - GET/PUT/PATCH/DELETE /api/v1/profiles/{slug}/
# - GET /api/v1/profiles/my-profile/
# - PATCH /api/v1/profiles/update-profile/
# - POST /api/v1/profiles/upload-avatar/
router.register(prefix="", viewset=ProfileViewSet, basename="profiles")

# Combine router-generated URLs into the urlpatterns
urlpatterns: List[URLPattern] = [
    path(
        route="",
        view=include(router.urls),
    ),
]
