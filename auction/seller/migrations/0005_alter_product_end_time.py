# Generated by Django 5.0.2 on 2024-03-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_alter_product_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='end_time',
            field=models.DateTimeField(),
        ),
    ]