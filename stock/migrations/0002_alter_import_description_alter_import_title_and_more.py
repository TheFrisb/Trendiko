# Generated by Django 5.0.1 on 2024-02-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="import",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Опис"),
        ),
        migrations.AlterField(
            model_name="import",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Име на увоз"),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="label",
            field=models.CharField(max_length=255, verbose_name="Label"),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="qr_code",
            field=models.ImageField(
                blank=True,
                upload_to="stock_items/qr_codes/%Y/%m/%d/",
                verbose_name="QR Code",
            ),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="sku",
            field=models.CharField(max_length=255, unique=True, verbose_name="SKU"),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="stock",
            field=models.PositiveIntegerField(default=0, verbose_name="Залиха"),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Наслов"),
        ),
    ]
