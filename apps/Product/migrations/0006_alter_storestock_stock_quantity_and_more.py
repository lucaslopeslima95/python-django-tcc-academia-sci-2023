# Generated by Django 4.2.2 on 2023-07-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_rename_stock_storestock_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storestock',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
