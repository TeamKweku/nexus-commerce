import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    """End-to-end tests for category endpoints"""

    endpoint = reverse("categories:category-list")  # Updated URL name

    def test_list_categories(self, api_client, category_factory):
        """Test listing categories endpoint"""
        # Create some test categories
        active_category = category_factory(name="Electronics", is_active=True)
        child_category = category_factory(
            name="Smartphones", parent=active_category, is_active=True
        )
        category_factory(name="Inactive Category", is_active=False)

        response = api_client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify response structure
        assert "categories" in data
        assert "count" in data["categories"]
        assert "results" in data["categories"]

        # Should return both active categories (parent and child)
        results = data["categories"]["results"]
        assert len(results) == 2

        # Verify parent category data
        parent_result = next(
            r for r in results if r["slug"] == active_category.slug
        )
        assert parent_result["category"] == "Electronics"
        assert parent_result["slug"] == "electronics"

        # Verify child category data
        child_result = next(
            r for r in results if r["slug"] == child_category.slug
        )
        assert child_result["category"] == "Smartphones"
        assert child_result["slug"] == "smartphones"

    def test_retrieve_category(self, api_client, category_factory):
        """Test retrieving a single category by slug"""
        category = category_factory(name="Test Category", is_active=True)
        url = reverse(
            "categories:category-detail", kwargs={"slug": category.slug}
        )

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify the response structure and content
        assert "categories" in data
        category_data = data["categories"]
        assert category_data["category"] == "Test Category"
        assert category_data["slug"] == "test-category"

    def test_retrieve_inactive_category(self, api_client, category_factory):
        """Test retrieving an inactive category returns 404"""
        category = category_factory(name="Inactive", is_active=False)
        url = reverse(
            "categories:category-detail", kwargs={"slug": category.slug}
        )

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
