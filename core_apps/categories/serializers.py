from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with nested representation.
    """

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "is_active",
            "children",
        ]

    def get_children(self, obj):
        """
        Get all active children categories.
        """
        children = obj.get_children().filter(is_active=True)
        serializer = CategorySerializer(children, many=True)
        return serializer.data
