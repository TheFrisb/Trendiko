# Generated by Django 5.0.1 on 2024-05-06 18:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0029_order_pdf_invoice"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="reserved_stock_items",
        ),
    ]
