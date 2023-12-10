# Generated by Django 5.0 on 2023-12-10 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0003_cartitem_type"),
        ("shop", "0006_productattribute"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="attribute",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.productattribute",
            ),
        ),
    ]
