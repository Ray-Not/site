# Generated by Django 5.0 on 2024-09-16 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_review_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='doors', to='web.tag'),
        ),
    ]