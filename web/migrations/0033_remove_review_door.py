# Generated by Django 5.0 on 2024-09-26 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_alter_review_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='door',
        ),
    ]
