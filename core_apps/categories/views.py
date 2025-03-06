from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from core_apps.common.renderers import GenericJSONRenderer
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [GenericJSONRenderer]
    object_label = "categories"
    lookup_field = "slug"
    http_method_names = ["get"]  # Read-only operations

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Get a list of all active categories",
        responses={200: CategorySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Get details of a specific category by slug",
        responses={
            200: CategorySerializer,
            404: "Category not found"
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
