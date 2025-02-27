from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Create a Swagger/OpenAPI schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Nexus Commerce API",
        default_version="v1",
        description="Building a scalable & secure e-commerce platform backend",
        contact=openapi.Contact(email="djangotuts2022@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Make documentation publicly accessible
    permission_classes=[permissions.AllowAny],  # Allow any user to view docs
)


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
]


admin.site.site_header = "Nexus Commerce Admin"
admin.site.site_title = "Nexus Commerce Admin Portal"
admin.site.index_title = "Welcome to Nexus Commerce Admin Portal"
