# Generated by Django 5.0.1 on 2024-05-21 03:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0007_alter_campaignentry_advertisement_cost"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaignentry",
            name="for_date",
        ),
    ]