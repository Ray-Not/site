# Generated by Django 5.0 on 2024-09-17 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_tag_text_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='text_color',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='dark', help_text='Выбор цвета текста', max_length=10),
        ),
    ]
