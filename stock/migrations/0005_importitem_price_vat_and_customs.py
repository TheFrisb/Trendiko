# Generated by Django 5.0.1 on 2024-02-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0004_alter_importitem_options_alter_stockitem_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="importitem",
            name="price_vat_and_customs",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Цена со ДДВ и царина"
            ),
        ),
    ]
