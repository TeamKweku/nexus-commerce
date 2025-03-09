from typing import Any

from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from core_apps.common.renderers import GenericJSONRenderer

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing categories.

    Attributes:
        queryset: QuerySet of active categories
        serializer_class: Serializer for Category model
        permission_classes: List of permission classes
        renderer_classes: List of renderer classes
        object_label: Label for the object type
        lookup_field: Field used for object lookup
        http_method_names: Allowed HTTP methods (read-only)
    """

    queryset: QuerySet[Category] = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [GenericJSONRenderer]
    object_label: str = "categories"
    lookup_field: str = "slug"
    http_method_names: list[str] = ["get"]  # Read-only operations

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Get a list of all active categories",
        responses={200: CategorySerializer(many=True)},
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        List all active categories.

        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Response: List of serialized categories
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Get details of a specific category by slug",
        responses={200: CategorySerializer, 404: "Category not found"},
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a specific category by slug.

        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Response: Serialized category data
        """
        return super().retrieve(request, *args, **kwargs)
