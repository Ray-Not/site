# Generated by Django 5.0 on 2024-09-17 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='color',
            new_name='color_hex',
        ),
    ]