# Generated by Django 5.0 on 2023-12-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('out_of_stock', 'Out of Stock'), ('archived', 'Archived')], default='archived', max_length=20),
        ),
    ]
