# Generated by Django 5.0 on 2024-10-12 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0058_alter_catalog_custom_h1'),
    ]

    operations = [
        migrations.AddField(
            model_name='door',
            name='h1',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='door',
            name='description',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
