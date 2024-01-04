# Generated by Django 5.0 on 2024-01-04 00:18

import django.db.models.deletion
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "thumbnail",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True, null=True, upload_to="products/%Y/%m/%d/"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "Published"),
                            ("out_of_stock", "Out of Stock"),
                            ("archived", "Archived"),
                        ],
                        default="published",
                        max_length=20,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("simple", "Simple"), ("variable", "Variable")],
                        default="simple",
                        max_length=20,
                    ),
                ),
                ("title", models.CharField(max_length=140)),
                ("regular_price", models.PositiveIntegerField()),
                ("sale_price", models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductAttribute",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("color", "Color"),
                            ("size", "Size"),
                            ("offer", "Offer"),
                            ("cart_offer", "Cart Offer"),
                        ],
                        default="color",
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(max_length=140)),
                ("content", models.CharField(max_length=140)),
                ("price", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributes",
                        to="shop.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
