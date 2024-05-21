# Generated by Django 5.0.1 on 2024-05-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0006_campaignentry_for_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignentry",
            name="advertisement_cost",
            field=models.FloatField(default=0, verbose_name="Total Advertisement Cost"),
        ),
    ]
