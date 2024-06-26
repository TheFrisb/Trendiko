# Generated by Django 5.0.1 on 2024-04-15 22:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0036_category_background_image_category_css"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="css",
        ),
        migrations.AddField(
            model_name="category",
            name="banner_css",
            field=models.TextField(
                blank=True, null=True, verbose_name="Banner CSS (стави !important)"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="discount_bar_css",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Discount Bar CSS (стави !important)",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="headline_css",
            field=models.TextField(
                blank=True, null=True, verbose_name="Headline CSS (стави !important)"
            ),
        ),
    ]
