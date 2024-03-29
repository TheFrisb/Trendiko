# Generated by Django 5.0.1 on 2024-01-26 14:42

import django.db.models.deletion
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0003_product_category_alter_category_promotion_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("rating", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=140)),
                ("content", models.TextField(blank=True, null=True)),
                (
                    "image",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True, null=True, upload_to="products/%Y/%m/%d/"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="shop.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
