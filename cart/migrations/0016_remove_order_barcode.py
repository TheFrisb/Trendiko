# Generated by Django 5.0.1 on 2024-03-31 14:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0015_rename_barcode_image_order_barcode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="barcode",
        ),
    ]
