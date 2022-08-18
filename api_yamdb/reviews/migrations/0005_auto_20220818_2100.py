# Generated by Django 2.2.16 on 2022-08-18 16:00

import reviews.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_merge_20220818_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.TextField(max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, validators=[reviews.validator.year_validate], verbose_name='Год'),
        ),
    ]
