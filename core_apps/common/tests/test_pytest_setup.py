import pytest
from django.conf import settings


def test_pytest_configuration():
    """Test that pytest is configured correctly with Django settings."""
    # Check that Django settings are properly loaded
    assert hasattr(settings, "INSTALLED_APPS")
    assert "core_apps.common" in settings.INSTALLED_APPS
    assert settings.DEBUG is True  # Should be True in local settings


def test_simple_addition():
    """A trivial test to verify pytest is running."""
    assert 1 + 1 == 2


@pytest.mark.django_db
def test_database_connection():
    """Test that we can connect to the database."""
    # This test will fail if the database connection is not configured correctly
    from django.db import connections

    connection = connections["default"]
    connection.ensure_connection()
    assert connection.is_usable()
