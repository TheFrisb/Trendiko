# Generated by Django 5.0.1 on 2024-05-21 07:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0012_pricechange"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricechange",
            name="counter",
            field=models.IntegerField(default=-1),
        ),
    ]