# Generated by Django 2.2.16 on 2022-08-17 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220817_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created',
        ),
    ]
