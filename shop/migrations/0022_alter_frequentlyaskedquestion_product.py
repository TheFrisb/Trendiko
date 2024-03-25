# Generated by Django 5.0.1 on 2024-03-16 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0021_frequentlyaskedquestion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frequentlyaskedquestion",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="faqItems",
                to="shop.product",
                verbose_name="Производ",
            ),
        ),
    ]