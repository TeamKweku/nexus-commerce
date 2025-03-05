from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer, ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing products.
    """

    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_queryset(self):
        """Return only active products with related data"""
        return self.queryset.select_related('category')\
            .filter(is_active=True)

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="""
        Retrieves a list of all active products.
        Only returns products that are marked as active.
        """,
        responses={
            200: ProductSerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Product",
        operation_description="""
        Retrieves a specific product by its slug.
        Returns 404 if product is not found or not active.
        """,
        responses={
            200: ProductSerializer,
            404: "Product not found",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Product",
        operation_description="Creates a new product.",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Invalid data",
            401: "Unauthorized",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Product",
        operation_description="Updates an existing product completely.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: "Invalid data",
            401: "Unauthorized",
            404: "Product not found",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Product",
        operation_description="Partially updates an existing product.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: "Invalid data",
            401: "Unauthorized",
            404: "Product not found",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Product",
        operation_description="Deletes an existing product.",
        responses={
            204: "Product deleted successfully",
            401: "Unauthorized",
            404: "Product not found",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
