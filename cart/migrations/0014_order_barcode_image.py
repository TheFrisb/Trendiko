# Generated by Django 5.0.1 on 2024-03-26 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0013_shippingdetails_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="barcode_image",
            field=models.ImageField(blank=True, null=True, upload_to="barcodes/"),
        ),
    ]
