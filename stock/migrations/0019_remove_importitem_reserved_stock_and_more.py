# Generated by Django 5.0.1 on 2024-05-19 05:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0018_remove_importitem_ad_spend_import_ad_spend"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="importitem",
            name="reserved_stock",
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="stock",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Вистинска залиха"
            ),
        ),
    ]
