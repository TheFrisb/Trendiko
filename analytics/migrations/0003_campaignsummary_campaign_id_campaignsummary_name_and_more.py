# Generated by Django 5.0.1 on 2024-05-17 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0002_remove_campaignsummary_campaign_id_and_more"),
        ("shop", "0046_alter_shopclient_options_shopclient_display_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaignsummary",
            name="campaign_id",
            field=models.CharField(default="1", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="campaignsummary",
            name="name",
            field=models.CharField(default="1", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="campaignsummary",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shop.product",
            ),
        ),
    ]