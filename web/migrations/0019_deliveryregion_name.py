# Generated by Django 5.0 on 2024-09-21 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_alter_blog_slug_alter_deliveryregion_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryregion',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
