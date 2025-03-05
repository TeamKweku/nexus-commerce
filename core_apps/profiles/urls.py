from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

app_name = "profiles"

router = DefaultRouter()
router.register("", ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
]
