from typing import Any, Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import (
    Attribute,
    AttributeValue,
    Product,
    ProductAttributeValue,
    ProductImage,
    ProductLine,
)


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    Used as nested serializer within ProductLineSerializer.

    Attributes:
        alternative_text: Alternative text for image accessibility
        url: URL to the stored image
        order: Display order of the image
    """

    class Meta:
        model = ProductImage
        fields: list[str] = [
            "alternative_text",
            "url",
            "order",
        ]


class AttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for product attributes.
    Provides basic attribute information.

    Attributes:
        name: Name of the attribute
        id: Unique identifier for the attribute
    """

    class Meta:
        model = Attribute
        fields: tuple[str, str] = ("name", "id")


class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer for attribute values with nested attribute information.

    Attributes:
        attribute: Nested AttributeSerializer instance
        attribute_value: Value of the attribute
    """

    attribute: AttributeSerializer = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields: tuple[str, str] = (
            "attribute",
            "attribute_value",
        )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductAttributeValue model.
    Maps attribute values to specific products.

    Attributes:
        attribute: Nested attribute information from source attribute_value
        value: String representation of the attribute value
    """

    attribute: AttributeSerializer = AttributeSerializer(
        source="attribute_value.attribute"
    )
    value: serializers.CharField = serializers.CharField(
        source="attribute_value.value"
    )

    class Meta:
        model = ProductAttributeValue
        fields: list[str] = ["attribute", "value"]


class ProductLineSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductLine model with nested product images.
    Handles variant-specific information for products.

    Attributes:
        product_images: Nested serializer for product images
        price: Product variant price
        sku: Stock keeping unit
        stock_qty: Available quantity
        weight: Product weight
        order: Display order
    """

    product_images: ProductImageSerializer = ProductImageSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = ProductLine
        fields: list[str] = [
            "id",
            "price",
            "sku",
            "stock_qty",
            "weight",
            "order",
            "product_images",
        ]
        read_only_fields: list[str] = ["created_at", "updated_at"]

    def validate_price(self, value: float) -> float:
        """
        Validate price is within acceptable range.

        Args:
            value: Price value to validate

        Returns:
            float: Validated price value

        Raises:
            ValidationError: If price is not within acceptable range
        """
        if value <= 0:
            raise serializers.ValidationError(
                _("Price must be greater than zero.")
            )
        if value >= 100000:
            raise serializers.ValidationError(_("Price cannot exceed 99999.99"))
        return value

    def validate_sku(self, value: str) -> str:
        """
        Validate SKU format.

        Args:
            value: SKU string to validate

        Returns:
            str: Validated SKU string

        Raises:
            ValidationError: If SKU exceeds length limit
        """
        if len(value) > 10:
            raise serializers.ValidationError(
                _("SKU cannot exceed 10 characters.")
            )
        return value

    def validate_stock_qty(self, value: int) -> int:
        """
        Validate stock quantity is non-negative.

        Args:
            value: Stock quantity to validate

        Returns:
            int: Validated stock quantity

        Raises:
            ValidationError: If stock quantity is negative
        """
        if value < 0:
            raise serializers.ValidationError(
                _("Stock quantity cannot be negative.")
            )
        return value

    def validate_weight(self, value: float) -> float:
        """
        Validate weight is positive.

        Args:
            value: Weight value to validate

        Returns:
            float: Validated weight value

        Raises:
            ValidationError: If weight is not positive
        """
        if value <= 0:
            raise serializers.ValidationError(
                _("Weight must be greater than zero.")
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer with nested ProductLines and attributes.
    Handles main product information and its relationships.

    Attributes:
        product_lines: Nested serializer for product variants
        category: Category name string
        attribute_value: Nested serializer for product attributes
    """

    product_lines: ProductLineSerializer = ProductLineSerializer(
        many=True, required=False
    )
    category: serializers.CharField = serializers.CharField(
        source="category.name"
    )
    attribute_value: AttributeValueSerializer = AttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields: list[str] = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "attribute_value",
            "product_lines",
        ]
        read_only_fields: list[str] = ["created_at", "slug"]

    def to_representation(self, instance: Product) -> Dict[str, Any]:
        """
        Custom representation of product data.
        Transforms attribute values into a specification dictionary.

        Args:
            instance: Product instance being serialized

        Returns:
            Dict[str, Any]: Transformed product data
        """
        data = super().to_representation(instance)
        if "attribute_value" in data:
            av_data = data.pop("attribute_value")
            attr_values = {}
            for key in av_data:
                attr_values.update(
                    {key["attribute"]["name"]: key["attribute_value"]}
                )
            data.update({"specification": attr_values})
        return data


class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product listings.
    Used when displaying product list views.

    Attributes:
        category_name: Name of the product category
    """

    category_name: serializers.CharField = serializers.CharField(
        source="category.name"
    )

    class Meta:
        model = Product
        fields: list[str] = [
            "name",
            "slug",
            "category_name",
            "is_digital",
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for products when listed by category.
    Includes minimal product information needed for category listing.

    Attributes:
        product_lines: Nested serializer for product variants
    """

    product_lines: ProductLineSerializer = ProductLineSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Product
        fields: list[str] = [
            "name",
            "slug",
            "description",
            "product_lines",
        ]
