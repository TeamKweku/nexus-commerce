from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core_apps.common.renderers import GenericJSONRenderer

from .models import Product, ProductImage, ProductLine
from .serializers import ProductCategorySerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing products with optimized database queries.
    Create, update, and delete operations restricted to admin interface.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [GenericJSONRenderer]
    lookup_field = "slug"
    object_label = "products"
    http_method_names = ["get"]

    # Add filter backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "is_digital"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return optimized queryset with all related data"""
        return (
            self.queryset.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch("attribute_values__attribute"),
                Prefetch(
                    "product_lines",
                    queryset=ProductLine.objects.filter(
                        is_active=True
                    ).order_by("order"),
                ),
                Prefetch(
                    "product_lines__product_images",
                    queryset=ProductImage.objects.filter(order=1),
                ),
                Prefetch("product_lines__attribute_value__attribute"),
            )
        )

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieves a list of all active products with "
        "optimized related data.",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Product",
        operation_description="Retrieves a specific product by slug with all "
        "related data.",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=False, methods=["get"], url_path=r"category/(?P<slug>[\w-]+)"
    )
    @swagger_auto_schema(
        operation_summary="List Products by Category",
        operation_description="Retrieves all products for a specific category.",
        responses={
            200: ProductCategorySerializer(many=True),
            404: "Category not found",
        },
    )
    def list_by_category(self, request, slug=None):
        """Return products filtered by category slug"""
        queryset = self.get_queryset().filter(category__slug=slug)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductCategorySerializer(queryset, many=True)
        return Response(
            {"count": len(serializer.data), "results": serializer.data}
        )
