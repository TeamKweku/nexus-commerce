from rest_framework import serializers

from core_apps.categories.serializers import CategorySerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer with optimized data representation.
    Handles both detailed and list views of products.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "category",
            "category_id",
            "is_digital",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["created_at", "slug"]

    def to_representation(self, instance):
        """
        Customize the final representation of the product data.
        """
        data = super().to_representation(instance)
        
        # Simplify category representation
        if data.get('category'):
            data['category'] = {
                'name': data['category']['category'],
                'slug': data['category']['slug']
            }
            
        return data


class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product listings.
    """
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "category_name",
            "is_digital",
            "is_active",
        ]
