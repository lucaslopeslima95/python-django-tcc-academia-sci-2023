# Generated by Django 4.2.2 on 2023-06-26 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Purchase', '0002_rename_fk_product_purchaseitem_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='quantity',
        ),
    ]