# Generated by Django 5.0.1 on 2024-06-05 21:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0020_alter_import_ad_spend"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockitem",
            name="stock",
            field=models.PositiveIntegerField(default=0, verbose_name="Залиха"),
        ),
    ]
