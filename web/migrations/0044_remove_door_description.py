# Generated by Django 5.0 on 2024-10-08 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0043_door_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='door',
            name='description',
        ),
    ]
