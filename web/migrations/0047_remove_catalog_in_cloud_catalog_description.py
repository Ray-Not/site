# Generated by Django 5.0 on 2024-10-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0046_door_catalogs_cloud'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='in_cloud',
        ),
        migrations.AddField(
            model_name='catalog',
            name='description',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
