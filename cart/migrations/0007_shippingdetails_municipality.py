# Generated by Django 5.0.1 on 2024-03-17 02:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0006_orderitem_is_from_promotion"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingdetails",
            name="municipality",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
