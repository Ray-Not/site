# Generated by Django 5.0 on 2024-10-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0044_remove_door_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='door',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
