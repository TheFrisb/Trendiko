# Generated by Django 5.0.1 on 2024-05-17 07:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaignsummary",
            name="campaign_id",
        ),
        migrations.RemoveField(
            model_name="campaignsummary",
            name="name",
        ),
        migrations.RemoveField(
            model_name="campaignsummary",
            name="product",
        ),
    ]
