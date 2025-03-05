# Generated by Django 4.2.11 on 2025-03-05 08:54

import autoslug.fields
import core_apps.categories.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                populate_from=core_apps.categories.models.get_category_slug,
                unique=True,
            ),
        ),
    ]
