# Generated by Django 5.0.1 on 2024-05-16 02:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0002_globalcss"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoredCounter",
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
                    "type",
                    models.CharField(
                        choices=[("price_change", "Price change")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]