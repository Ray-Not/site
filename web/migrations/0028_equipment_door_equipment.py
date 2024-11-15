# Generated by Django 5.0 on 2024-09-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_alter_deliveryregion_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='doors_equip/')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='door',
            name='equipment',
            field=models.ManyToManyField(blank=True, related_name='doors', to='web.equipment'),
        ),
    ]
