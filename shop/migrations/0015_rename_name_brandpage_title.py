# Generated by Django 5.0.1 on 2024-03-03 16:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0014_brandpage_alter_category_promotion_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="brandpage",
            old_name="name",
            new_name="title",
        ),
    ]