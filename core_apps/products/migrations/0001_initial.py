import autoslug.fields
import core_apps.products.fields
import core_apps.products.models
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("categories", "0002_alter_category_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Format: required, max-length=100",
                        max_length=100,
                        verbose_name="Product Name",
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=core_apps.products.models.get_product_slug,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Format: optional",
                        verbose_name="Description",
                    ),
                ),
                (
                    "is_digital",
                    models.BooleanField(
                        default=False,
                        help_text="Format: true=Digital Product, false=Physical Product",
                        verbose_name="Digital Product",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text="Format: true=product visible",
                        verbose_name="Product Visibility",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Format: required, reference to Category",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="categories.category",
                        verbose_name="Product Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProductLine",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Format: maximum price 999.99, decimal places 2",
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="Price",
                    ),
                ),
                (
                    "sku",
                    models.CharField(
                        help_text="Format: required, unique, max-length=10",
                        max_length=10,
                        unique=True,
                        verbose_name="Stock Keeping Unit",
                    ),
                ),
                (
                    "stock_qty",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Format: required, default=0",
                        verbose_name="Stock Quantity",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text="Format: true=product line is active",
                        verbose_name="Is Active",
                    ),
                ),
                (
                    "weight",
                    models.FloatField(
                        help_text="Format: required, in kilograms",
                        verbose_name="Weight",
                    ),
                ),
                (
                    "order",
                    core_apps.products.fields.OrderField(
                        blank=True,
                        default=1,
                        help_text="Format: auto-assigned if not specified",
                        verbose_name="Display Order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Format: required, references Product model",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_lines",
                        to="products.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Line",
                "verbose_name_plural": "Product Lines",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "alternative_text",
                    models.CharField(
                        help_text="Format: required, max-length=100",
                        max_length=100,
                        verbose_name="Alternative Text",
                    ),
                ),
                (
                    "url",
                    models.ImageField(
                        default="product_images/default.jpg",
                        help_text="Format: required, default image provided",
                        upload_to="product_images/",
                        verbose_name="Image URL",
                    ),
                ),
                (
                    "order",
                    core_apps.products.fields.OrderField(
                        blank=True,
                        help_text="Format: auto-assigned if not specified",
                        verbose_name="Display Order",
                    ),
                ),
                (
                    "product_line",
                    models.ForeignKey(
                        help_text="Format: required, references ProductLine",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_images",
                        to="products.productline",
                        verbose_name="Product Line",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
                "ordering": ["order"],
            },
        ),
    ]
