# Generated by Django 5.0.1 on 2024-04-07 23:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0023_rename_name_abandonedcartdetails_full_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[("active", "Активна"), ("abandoned", "Напуштена")],
                db_index=True,
                default="active",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="abandonedcartdetails",
            name="address",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="abandonedcartdetails",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="abandonedcartdetails",
            name="phone",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
