import factory

from core_apps.categories.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for Category model"""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"test_category_{n}")
    # Remove the explicit slug definition to let AutoSlugField handle it
