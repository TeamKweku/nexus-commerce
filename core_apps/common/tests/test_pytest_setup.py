from django.conf import settings


def test_pytest_configuration():
    """Test that pytest is configured correctly with Django settings."""
    # Check that Django settings are properly loaded
    assert hasattr(settings, "INSTALLED_APPS")
    assert "core_apps.common" in settings.INSTALLED_APPS

    # For now, let's check that settings are loaded rather than specific values
    assert hasattr(settings, "DEBUG"), "DEBUG setting is not defined"


def test_simple_addition():
    """A trivial test to verify pytest is running."""
    assert 1 + 1 == 2
