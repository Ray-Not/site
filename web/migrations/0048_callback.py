# Generated by Django 5.0 on 2024-10-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0047_remove_catalog_in_cloud_catalog_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=18)),
            ],
        ),
    ]