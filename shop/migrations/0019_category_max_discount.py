# Generated by Django 5.0.1 on 2024-03-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0018_rename_content_productattribute_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="max_discount",
            field=models.PositiveIntegerField(
                default=50, verbose_name="Максимален попуст"
            ),
            preserve_default=False,
        ),
    ]