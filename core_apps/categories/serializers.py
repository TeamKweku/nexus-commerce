from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with a cleaner frontend-friendly
    representation.
    """

    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = [
            "category",
            "slug",
        ]

    def get_children(self, obj):
        """Get all active children categories."""
        children = obj.get_children().filter(is_active=True)
        serializer = CategorySerializer(children, many=True)
        return serializer.data
