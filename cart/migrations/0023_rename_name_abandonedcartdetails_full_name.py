# Generated by Django 5.0.1 on 2024-04-07 22:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0022_alter_abandonedcartdetails_city_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="abandonedcartdetails",
            old_name="name",
            new_name="full_name",
        ),
    ]