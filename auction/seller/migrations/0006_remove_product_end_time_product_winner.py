# Generated by Django 5.0.2 on 2024-03-02 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_alter_buyerprofilemodel_buyer'),
        ('seller', '0005_alter_product_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='end_time',
        ),
        migrations.AddField(
            model_name='product',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_products', to='buyer.buyermodel'),
        ),
    ]
