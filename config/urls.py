from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Nexus Commerce API",
        default_version="v1",
        description="""
        Nexus Commerce REST API documentation.
        ## Authentication
        This API uses JWT tokens stored in HTTP-only cookies for authentication.
        ### Available Authentication Methods:
        - Email/Password login
        - Social authentication (Google, Facebook)
        - Token refresh
        ### Security
        - All tokens are stored as HTTP-only cookies
        - CSRF protection enabled
        - Rate limiting applied
        ## Djoser Authentication Endpoints
        This API includes several authentication endpoints provided by Djoser:
        ### User Registration and Activation
        - POST /api/v1/auth/users/ - Register new user
        - POST /api/v1/auth/users/activation/ - Activate user account
        - POST /api/v1/auth/users/resend_activation/ - Resend activation email
        ### Password Management
        - POST /api/v1/auth/users/reset_password/ - Request password reset
        - POST /api/v1/auth/users/reset_password_confirm/ - Confirm password
        - POST /api/v1/auth/users/set_password/ - Change password
        ### Account Management
        - POST /api/v1/auth/users/set_username/ - Change username
        """,
        terms_of_service="https://www.nexuscommerce.com/terms/",
        contact=openapi.Contact(email="djangotuts2022@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        path("api/v1/auth/", include("djoser.urls")),
        path("api/v1/auth/", include("core_apps.users.urls")),
        path("api/v1/profiles/", include("core_apps.profiles.urls")),
        path("api/v1/categories/", include("core_apps.categories.urls")),
        path("api/v1/products/", include("core_apps.products.urls")),
    ],
)

urlpatterns = [
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
    path("jet/", include("jet.urls", "jet")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/categories/", include("core_apps.categories.urls")),
    path("api/v1/products/", include("core_apps.products.urls")),
]


admin.site.site_header = "Nexus Commerce Admin"
admin.site.site_title = "Nexus Commerce Admin Portal"
admin.site.index_title = "Welcome to Nexus Commerce Admin Portal"
