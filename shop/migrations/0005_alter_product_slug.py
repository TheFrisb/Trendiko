# Generated by Django 5.0.1 on 2024-01-28 22:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
