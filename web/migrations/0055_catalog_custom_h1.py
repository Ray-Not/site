# Generated by Django 5.0 on 2024-10-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0054_catalog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='custom_h1',
            field=models.CharField(default='Входные металлические {{ catalog.title|lower }} двери', max_length=512),
        ),
    ]
