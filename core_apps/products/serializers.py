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
    """

    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("name", "id")


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = (
            "attribute",
            "attribute_value",
        )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for ProductAttributeValue model"""

    attribute = AttributeSerializer(source="attribute_value.attribute")
    value = serializers.CharField(source="attribute_value.value")

    class Meta:
        model = ProductAttributeValue
        fields = ["attribute", "value"]


class ProductLineSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductLine model with nested product images.
    """

    product_images = ProductImageSerializer(many=True, read_only=True)
    attribute_value = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_qty",
            "weight",
            "order",
            "product_images",
            "attribute_value",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def to_representation(self, instance):
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

    def validate_price(self, value):
        """Validate price is within acceptable range"""
        if value <= 0:
            raise serializers.ValidationError(
                _("Price must be greater than zero.")
            )
        if value >= 100000:
            raise serializers.ValidationError(_("Price cannot exceed 99999.99"))
        return value

    def validate_sku(self, value):
        """Validate SKU format"""
        if len(value) > 10:
            raise serializers.ValidationError(
                _("SKU cannot exceed 10 characters.")
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer with nested ProductLines and attributes.
    """

    product_lines = ProductLineSerializer(many=True, required=False)
    category = serializers.CharField(source="category.name")
    attribute_value = AttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "category",
            "attribute_value",
            "product_lines",
        ]
        read_only_fields = ["created_at", "slug"]

    def to_representation(self, instance):
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
    """

    category_name = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "category_name",
            "is_digital",
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for products when listed by category.
    Includes minimal product information needed for category listing.
    """

    product_lines = ProductLineSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "product_lines",
        ]
