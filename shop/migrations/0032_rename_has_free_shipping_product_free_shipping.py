# Generated by Django 5.0.1 on 2024-03-31 23:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0031_product_technical_specifications"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="has_free_shipping",
            new_name="free_shipping",
        ),
    ]
