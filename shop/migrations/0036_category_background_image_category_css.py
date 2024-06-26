# Generated by Django 5.0.1 on 2024-04-15 16:00

import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0035_alter_category_display_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="background_image",
            field=imagekit.models.fields.ProcessedImageField(
                blank=True,
                null=True,
                upload_to="categories/%Y/%m/%d/",
                verbose_name="Позадинска слика",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="css",
            field=models.TextField(blank=True, null=True, verbose_name="CSS"),
        ),
    ]
