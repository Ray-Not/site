# Generated by Django 5.0 on 2024-09-20 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_door_catalogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=512),
        ),
    ]
