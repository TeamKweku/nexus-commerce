# Generated by Django 4.2.11 on 2025-03-06 07:50

import autoslug.fields
import cloudinary.models
import core_apps.profiles.models
from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "user_type",
                    models.CharField(
                        choices=[
                            ("buyer", "Buyer"),
                            ("seller", "Seller"),
                            ("admin", "Admin"),
                        ],
                        default="buyer",
                        max_length=20,
                        verbose_name="User Type",
                    ),
                ),
                (
                    "avatar",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="Avatar"
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True, verbose_name="Bio")),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Enter phone number in international format (e.g., +233123456789)",
                        max_length=30,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        default="Accra", max_length=180, verbose_name="City"
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=core_apps.profiles.models.get_user_username,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
            },
        ),
    ]
