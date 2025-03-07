from typing import Any, Dict, List, Optional, Set, Tuple

from django.core.cache import cache
from django.db.models import Prefetch, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from core_apps.common.renderers import GenericJSONRenderer

from .models import Product, ProductImage, ProductLine
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing products with optimized database queries.
    Create, update, and delete operations restricted to admin interface.

    Attributes:
        queryset: Base queryset for all product operations
        serializer_class: Main serializer for product data
        permission_classes: List of permission classes controlling access
        renderer_classes: List of classes handling response rendering
        lookup_field: Field used for object lookup (slug)
        object_label: Label used for object identification
        http_method_names: Allowed HTTP methods (read-only)
        filter_backends: List of filter backend classes
        filterset_fields: Fields available for filtering
        search_fields: Fields available for text search
        ordering_fields: Fields available for sorting
        ordering: Default ordering
    """

    queryset: QuerySet[Product] = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes: List[Any] = [IsAuthenticatedOrReadOnly]
    renderer_classes: List[Any] = [GenericJSONRenderer]
    lookup_field: str = "slug"
    object_label: str = "products"
    http_method_names: List[str] = ["get"]

    filter_backends: List[Any] = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields: List[str] = ["category", "is_digital"]
    search_fields: List[str] = ["name", "description"]
    ordering_fields: List[str] = ["created_at", "name"]
    ordering: List[str] = ["-created_at"]

    def get_cache_key(self, **kwargs: Dict[str, Any]) -> str:
        """
        Generate cache key based on view parameters.

        Args:
            **kwargs: Additional parameters to include in cache key

        Returns:
            str: Generated cache key combining action, query params, and kwargs
        """
        query_params: Set[Tuple[str, str]] = frozenset(
            self.request.query_params.items()
        )
        key_parts: List[str] = [
            "product",
            self.action,
            str(query_params),
            str(kwargs),
        ]
        return ":".join(key_parts)

    def get_cached_queryset(
        self, **kwargs: Dict[str, Any]
    ) -> QuerySet[Product]:
        """
        Get queryset with caching support.

        This method:
        1. Generates a cache key based on the request parameters
        2. Attempts to fetch the queryset from cache
        3. If not found, builds an optimized queryset with:
           - Active products only
           - Related category data
           - Prefetched related fields
           - Additional filters based on kwargs
        4. Caches the result for 15 minutes

        Args:
            **kwargs: Additional filters to apply to the queryset

        Returns:
            QuerySet[Product]: Filtered and optimized product queryset
        """
        cache_key: str = self.get_cache_key(**kwargs)
        result: Optional[QuerySet[Product]] = cache.get(cache_key)

        if result is None:
            queryset: QuerySet[Product] = (
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

            if "category_slug" in kwargs:
                queryset = queryset.filter(
                    category__slug=kwargs["category_slug"]
                )
            elif "product_slug" in kwargs:
                queryset = queryset.filter(slug=kwargs["product_slug"])

            cache.set(cache_key, queryset, timeout=60 * 15)
            return queryset

        return result

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieves a list of all active products with"
        " optimized related data.",
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        List all active products with pagination support.

        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Response: Paginated list of products
        """
        queryset: QuerySet[Product] = self.get_cached_queryset()
        page: Optional[List[Product]] = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve Product",
        operation_description="Retrieves a specific product by slug "
        "with all related data.",
        responses={200: ProductSerializer, 404: "Product not found"},
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve a specific product by slug.

        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Response: Single product details
        """
        instance: Optional[Product] = self.get_cached_queryset(
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
    def list_by_category(
        self, request: Request, slug: Optional[str] = None
    ) -> Response:
        """
        List all products in a specific category.

        Args:
            request: HTTP request object
            slug: Category slug to filter by

        Returns:
            Response: List of products in the specified category
        """
        queryset: QuerySet[Product] = self.get_cached_queryset(
            category_slug=slug
        )
        page: Optional[List[Product]] = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
