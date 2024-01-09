# Generated by Django 5.0.1 on 2024-01-09 00:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="cart",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="cartitem",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="cartitem",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="orderitem",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="orderitem",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="shippingdetails",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="shippingdetails",
            old_name="updated",
            new_name="updated_at",
        ),
    ]
