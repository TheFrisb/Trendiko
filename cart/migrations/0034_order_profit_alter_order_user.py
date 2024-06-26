# Generated by Django 5.0.1 on 2024-05-07 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0033_alter_order_user"),
        ("shop", "0044_shopclient"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="profit",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="shop.shopclient",
                verbose_name="Клиент",
            ),
        ),
    ]
