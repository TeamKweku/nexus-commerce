from typing import List

from django.urls import include, path
from django.urls.resolvers import URLPattern
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

# Application namespace for URL reversing
app_name: str = "products"

# Initialize the DefaultRouter for RESTful endpoints
router: DefaultRouter = DefaultRouter()

# Register the ProductViewSet with an empty prefix
# This creates the following URL patterns:
# - GET/POST /api/v1/products/
# - GET/PUT/PATCH/DELETE /api/v1/products/{slug}/
# - GET /api/v1/products/category/{slug}/
router.register(prefix="", viewset=ProductViewSet, basename="products")

# Combine router-generated URLs into the urlpatterns
urlpatterns: List[URLPattern] = [
    path(
        route="",
        view=include(router.urls),
    ),
]
