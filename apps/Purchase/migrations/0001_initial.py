# Generated by Django 4.2.2 on 2023-06-20 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0002_rename_deleted_product_is_deleted'),
        ('Collaborator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='deadLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DAY', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchase', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.IntegerField()),
                ('fk_collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Collaborator.collaborator')),
                ('fk_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
                ('fk_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Purchase.purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='fk_colaborattor',
            field=models.ManyToManyField(related_name='purchases', through='Purchase.PurchaseItem', to='Collaborator.collaborator'),
        ),
    ]