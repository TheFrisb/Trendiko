# Generated by Django 5.0 on 2024-01-04 00:18

import django.db.models.deletion
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Import",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StockItem",
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
                ("title", models.CharField(max_length=255)),
                (
                    "thumbnail",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True, null=True, upload_to="products/%Y/%m/%d/"
                    ),
                ),
                (
                    "qr_code",
                    models.ImageField(
                        blank=True, upload_to="stock_items/qr_codes/%Y/%m/%d/"
                    ),
                ),
                ("sku", models.CharField(max_length=255)),
                ("stock", models.PositiveIntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ImportItem",
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
                ("quantity", models.PositiveIntegerField(default=0)),
                ("price", models.PositiveIntegerField(default=0)),
                (
                    "parentImport",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stock.import"
                    ),
                ),
                (
                    "stock_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stock.stockitem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
