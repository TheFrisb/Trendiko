# Generated by Django 5.0.1 on 2024-05-16 02:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0003_storedcounter"),
    ]

    operations = [
        migrations.AddField(
            model_name="storedcounter",
            name="value",
            field=models.IntegerField(default=0),
        ),
    ]