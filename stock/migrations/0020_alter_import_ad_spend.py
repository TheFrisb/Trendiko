# Generated by Django 5.0.1 on 2024-05-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0019_remove_importitem_reserved_stock_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="import",
            name="ad_spend",
            field=models.FloatField(default=0, verbose_name="Ad Spend"),
        ),
    ]
