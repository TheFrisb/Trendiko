# Generated by Django 5.0 on 2023-12-09 14:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_product_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="name",
            new_name="title",
        ),
    ]
