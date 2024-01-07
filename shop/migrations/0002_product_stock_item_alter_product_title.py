# Generated by Django 5.0 on 2024-01-05 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
        ("stock", "0002_stockitem_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.stockitem",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
