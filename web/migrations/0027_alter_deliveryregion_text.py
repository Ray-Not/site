# Generated by Django 5.0 on 2024-09-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_alter_deliveryregion_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryregion',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
