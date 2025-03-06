from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from core_apps.common.renderers import GenericJSONRenderer

from .models import Category
from .serializers import CategorySerializer


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    renderer_classes = [GenericJSONRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active"]
    lookup_field = "slug"
    object_label = "categories"

    def get_queryset(self):
        """Return only active categories."""
        return Category.objects.filter(is_active=True)

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Get a paginated list of all active categories",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Category",
        operation_description="Create a new category",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Get a specific category by its slug",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Category",
        operation_description="Update all fields of a specific category",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Category",
        operation_description="Update specific fields of a category",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Category",
        operation_description="Delete a specific category",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
