import pytest
from django.db.utils import IntegrityError

from core_apps.categories.models import Category

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_output(self, category_factory):
        """Test the string representation of Category model"""
        obj = category_factory(name="test_cat")
        assert str(obj) == "test_cat"

    def test_name_unique_field(self, category_factory):
        """Test name field uniqueness"""
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(name="test_cat")

    def test_mptt_parent_child_relationship(self, category_factory):
        """Test MPTT parent-child relationship"""
        parent = category_factory(name="Parent")
        child = category_factory(name="Child", parent=parent)
        assert child.parent == parent
        assert parent in child.get_ancestors()

    def test_is_active_false_default(self, category_factory):
        """Test is_active field default value"""
        obj = category_factory(is_active=False)
        assert obj.is_active is False

    def test_parent_field_null(self, category_factory):
        """Test parent field can be null"""
        obj = category_factory()
        assert obj.parent is None

    def test_return_category_active_only(self, category_factory):
        """Test active categories filter"""
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.active().count()
        assert qs == 1
