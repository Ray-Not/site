# Generated by Django 5.0 on 2024-09-22 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0022_alter_deliveryregion_cost_alter_deliveryregion_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryregion',
            name='cost',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
