from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core_apps.common.renderers import GenericJSONRenderer

from .models import Product, ProductLine
from .serializers import ProductLineSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing products.
    Product lines are managed through the product endpoints.
    """

    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    serializer_class = ProductSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "products"

    def get_queryset(self):
        """Return only active products with related data"""
        return (
            self.queryset.select_related("category")
            .prefetch_related("product_lines")
            .filter(is_active=True)
        )
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


class ProductLineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing product lines.
    """

    serializer_class = ProductLineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductLine.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_active", "product"]
    search_fields = ["sku"]

    def get_queryset(self):
        """Return only active product lines with related data"""
        return self.queryset.select_related("product").filter(is_active=True)

    @swagger_auto_schema(
        operation_summary="List Product Lines",
        operation_description="Returns a list of all active product lines.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Product Line",
        operation_description="Creates a new product line variant.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Product Line",
        operation_description="Returns details of a specific product line.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Product Line",
        operation_description="Updates all fields of a specific product line.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Product Line",
        operation_description="Updates some fields of a specific product line.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Product Line",
        operation_description="Deletes a specific product line.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
