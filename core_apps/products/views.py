# from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core_apps.common.renderers import GenericJSONRenderer

from .models import Product, ProductImage, ProductLine
from .serializers import ProductSerializer


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

    def get_cache_key(self, **kwargs):
        """Generate cache key based on view parameters"""
        # Include query parameters in cache key
        query_params = frozenset(self.request.query_params.items())
        # Include any kwargs (like slug) in cache key
        key_parts = ["product", self.action, str(query_params), str(kwargs)]
        return ":".join(key_parts)

    def get_cached_queryset(self, **kwargs):
        """Get queryset with caching"""
        cache_key = self.get_cache_key(**kwargs)
        result = cache.get(cache_key)

        if result is None:
            queryset = (
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

            # Apply any additional filters from kwargs
            if "category_slug" in kwargs:
                queryset = queryset.filter(
                    category__slug=kwargs["category_slug"]
                )
            elif "product_slug" in kwargs:
                queryset = queryset.filter(slug=kwargs["product_slug"])

            # Cache for 15 minutes by default
            cache.set(cache_key, queryset, timeout=60 * 15)
            return queryset

        return result

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieves a list of all active products "
        "with optimized related data.",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_cached_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve Product",
        operation_description="Retrieves a specific product by slug with "
        "all related data.",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_cached_queryset(
            product_slug=kwargs.get("slug")
        ).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="List Products by Category",
        operation_description="Retrieves all products in a specific category.",
        responses={200: ProductSerializer(many=True)},
    )
    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_by_category(self, request, slug=None):
        queryset = self.get_cached_queryset(category_slug=slug)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
