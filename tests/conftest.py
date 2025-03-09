import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories.category import CategoryFactory
from tests.factories.product import (
    ProductFactory,
    ProductLineFactory,
    ProductTypeFactory,
)

User = get_user_model()

# Register factories
register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductTypeFactory)


@pytest.fixture
def category_factory():
    """
    Factory fixture for creating test categories
    Returns a function that creates Category instances with custom attributes
    """

    def create_category(**kwargs):
        return CategoryFactory(**kwargs)

    return create_category


@pytest.fixture
def product_factory():
    """
    Factory fixture for creating test products
    Returns a function that creates Product instances with custom attributes
    """

    def create_product(**kwargs):
        return ProductFactory(**kwargs)

    return create_product


@pytest.fixture
def product_line_factory():
    """
    Factory fixture for creating test product lines
    Returns a function that creates ProductLine instances with custom attributes
    """

    def create_product_line(**kwargs):
        return ProductLineFactory(**kwargs)

    return create_product_line


@pytest.fixture
def product_type_factory():
    """
    Factory fixture for creating test product types
    Returns a function that creates ProductType instances with custom attributes
    """

    def create_product_type(**kwargs):
        return ProductTypeFactory(**kwargs)

    return create_product_type


@pytest.fixture
def api_client():
    """
    Returns an instance of DRF APIClient for making test requests
    """
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db):
    """Fixture that creates an authenticated API client"""
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        is_active=True,
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
