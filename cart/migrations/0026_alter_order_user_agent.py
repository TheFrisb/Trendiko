# Generated by Django 5.0.1 on 2024-04-14 22:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0025_order_mail_is_sent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="user_agent",
            field=models.TextField(blank=True, null=True, verbose_name="User Agent"),
        ),
    ]