# Generated by Django 5.0.1 on 2024-03-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0009_reservedstockitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="importitem",
            name="quantity",
            field=models.PositiveIntegerField(
                db_index=True, default=0, verbose_name="Количина"
            ),
        ),
    ]