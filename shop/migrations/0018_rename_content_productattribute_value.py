# Generated by Django 5.0.1 on 2024-03-04 18:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0017_remove_productattribute_color"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productattribute",
            old_name="content",
            new_name="value",
        ),
    ]
