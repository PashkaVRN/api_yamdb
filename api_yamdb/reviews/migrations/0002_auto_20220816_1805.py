# Generated by Django 2.2.16 on 2022-08-16 13:05

import reviews.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, db_index=True, validators=[reviews.validator.year_validate], verbose_name='Год'),
        ),
    ]
