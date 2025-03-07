from typing import Any, Dict, List

from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with a cleaner frontend-friendly
    representation.

    Attributes:
        category: Renamed field that maps to the Category model's name field

    Meta:
        model: The Category model to serialize
        fields: List of fields to include in serialization
    """

    category: serializers.CharField = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = [
            "category",
            "slug",
        ]

    def get_children(self, obj: Category) -> List[Dict[str, Any]]:
        """
        Get all active children categories.

        Args:
            obj: Category instance being serialized

        Returns:
            List[Dict[str, Any]]: Serialized data of active child categories
        """
        children = obj.get_children().filter(is_active=True)
        serializer = CategorySerializer(children, many=True)
        return serializer.data
