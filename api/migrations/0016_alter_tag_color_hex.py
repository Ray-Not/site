# Generated by Django 5.1 on 2024-09-09 03:52

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_tag_color_hex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color_hex',
            field=models.CharField(help_text='Введите цвет в формате #RRGGBB', max_length=7, validators=[api.models.validate_hex_color]),
        ),
    ]
