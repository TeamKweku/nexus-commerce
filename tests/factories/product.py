import factory

from core_apps.products.models import Product, ProductLine, ProductType
from tests.factories.category import CategoryFactory


class ProductTypeFactory(factory.django.DjangoModelFactory):
    """Factory for ProductType model"""

    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: f"test_type_{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for Product model"""

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"test_product_{n}")
    description = factory.Faker("text")
    is_digital = False
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    """Factory for ProductLine model"""

    class Meta:
        model = ProductLine

    product = factory.SubFactory(ProductFactory)
    price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    sku = factory.Sequence(lambda n: f"SKU_{n}")
    stock_qty = factory.Faker("random_int", min=0, max=100)
    product_type = factory.SubFactory(ProductTypeFactory)
    is_active = True
    weight = factory.Faker("random_int", min=100, max=1000)
