# Generated by Django 5.0.1 on 2024-03-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0022_alter_frequentlyaskedquestion_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frequentlyaskedquestion",
            name="is_default",
            field=models.BooleanField(
                db_index=True,
                default=False,
                verbose_name="Стандардно прашање (Вклучено за секој производ)",
            ),
        ),
    ]
