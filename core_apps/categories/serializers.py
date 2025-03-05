from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with a cleaner frontend-friendly
    representation.
    """

    category = serializers.CharField(source="name")
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "category",
            "slug",
            "children",
            "description",
            "parent",
            "is_active",
        ]
        read_only_fields = ["id", "slug"]
        extra_kwargs = {
            "description": {"write_only": True},
            "parent": {"write_only": True},
            "is_active": {"write_only": True},
        }

    def get_children(self, obj):
        """Get all active children categories."""
        children = obj.get_children().filter(is_active=True)
        serializer = CategorySerializer(children, many=True)
        return serializer.data

    def validate_category(self, value):
        """
        Validate that the category name is unique.
        """
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                _("A category with this name already exists.")
            )
        return value
