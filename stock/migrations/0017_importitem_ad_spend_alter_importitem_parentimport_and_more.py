# Generated by Django 5.0.1 on 2024-05-19 02:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0016_alter_reservedstockitem_order_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="importitem",
            name="ad_spend",
            field=models.IntegerField(default=0, verbose_name="Ad Spend"),
        ),
        migrations.AlterField(
            model_name="importitem",
            name="parentImport",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="import_items",
                to="stock.import",
            ),
        ),
        migrations.AlterField(
            model_name="importitem",
            name="stock_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="import_items",
                to="stock.stockitem",
            ),
        ),
    ]
