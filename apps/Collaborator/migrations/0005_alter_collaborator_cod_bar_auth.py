# Generated by Django 4.2.2 on 2023-07-27 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collaborator', '0004_collaborator_cod_bar_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='cod_bar_auth',
            field=models.CharField(default='cd586a853cd2f36b38d315ee81adbf01', max_length=32),
        ),
    ]
