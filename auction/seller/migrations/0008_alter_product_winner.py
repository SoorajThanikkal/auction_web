# Generated by Django 5.0.2 on 2024-03-05 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_alter_buyerprofilemodel_buyer'),
        ('seller', '0007_alter_product_min_price_alter_product_pro_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_products', to='buyer.buyermodel'),
        ),
    ]
