# Generated by Django 5.0.1 on 2024-11-03 23:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0004_storedcounter_value"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "key",
                    models.CharField(max_length=255, unique=True, verbose_name="Име"),
                ),
                (
                    "enabled",
                    models.BooleanField(default=True, verbose_name="Овозможено"),
                ),
            ],
            options={
                "verbose_name": "Глобална поставка",
                "verbose_name_plural": "Глобални поставки",
            },
        ),
    ]
