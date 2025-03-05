from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

app_name = "products"

router = DefaultRouter()
router.register("", ProductViewSet, basename="products")  # Changed from "products" to ""

urlpatterns = [
    path("", include(router.urls)),
]
