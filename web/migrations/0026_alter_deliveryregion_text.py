# Generated by Django 5.0 on 2024-09-22 15:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_remove_deliveryregion_d_remove_deliveryregion_fill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryregion',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]