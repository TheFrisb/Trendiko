# Generated by Django 5.0.9 on 2024-11-19 02:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0008_globalcss_cart_section_five_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="globalcss",
            name="cart_section_six",
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="cart_section_five",
            field=models.TextField(default="", verbose_name="Cart Section 5"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="cart_section_four",
            field=models.TextField(default="", verbose_name="Cart Section 4"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="cart_section_one",
            field=models.TextField(default="", verbose_name="Cart Section 1"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="cart_section_three",
            field=models.TextField(default="", verbose_name="Cart Section 3"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="cart_section_two",
            field=models.TextField(default="", verbose_name="Cart Section 2"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="checkout_section_one",
            field=models.TextField(default="", verbose_name="Checkout Section 1"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="checkout_section_three",
            field=models.TextField(default="", verbose_name="Checkout Section 3"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="globalcss",
            name="checkout_section_two",
            field=models.TextField(default="", verbose_name="Checkout Section 2"),
            preserve_default=False,
        ),
    ]
