from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core_apps.categories.serializers import CategorySerializer

from .models import Product, ProductLine, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    Used as nested serializer within ProductLineSerializer.
    """
    class Meta:
        model = ProductImage
        fields = [
            "alternative_text",
            "url",
            "order"
        ]


class ProductLineSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductLine model with nested product images.
    """
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_qty",
            "weight",
            "product_images"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_price(self, value):
        """Validate price is within acceptable range"""
        if value <= 0:
            raise serializers.ValidationError(
                _("Price must be greater " "than zero.")
            )
        if value >= 1000:
            raise serializers.ValidationError(_("Price cannot exceed 999.99"))
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
    Product serializer with nested ProductLines.
    """
    product_lines = ProductLineSerializer(many=True)
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "category_name",
            "is_digital",
            "is_active",
            "created_at",
            "product_lines",
        ]
        read_only_fields = ["created_at", "slug"]

    def create(self, validated_data):
        product_lines_data = validated_data.pop("product_lines")
        product = Product.objects.create(**validated_data)

        for line_data in product_lines_data:
            ProductLine.objects.create(product=product, **line_data)

        return product

    def update(self, instance, validated_data):
        product_lines_data = validated_data.pop("product_lines", None)

        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update product lines if provided
        if product_lines_data is not None:
            instance.product_lines.all().delete()  # Remove existing lines
            for line_data in product_lines_data:
                ProductLine.objects.create(product=instance, **line_data)

        return instance


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
            "is_active",
        ]
