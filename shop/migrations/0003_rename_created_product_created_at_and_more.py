# Generated by Django 5.0.1 on 2024-01-09 00:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_product_stock_item_alter_product_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="productattribute",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="productattribute",
            old_name="updated",
            new_name="updated_at",
        ),
    ]
