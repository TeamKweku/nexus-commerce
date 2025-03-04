from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        """
        Return only root categories (no parent) that are active.
        """
        return Category.objects.filter(parent=None, is_active=True)

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="""
        Retrieves a list of all root categories.
        Only returns active categories with no parent.
        """,
        responses={
            200: CategorySerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="""
        Retrieves a specific category by its slug.
        Includes all child categories if present.
        """,
        responses={
            200: CategorySerializer,
            404: "Category not found",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Category",
        operation_description="Creates a new category.",
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: "Invalid data",
            401: "Unauthorized",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
