# Generated by Django 2.2.16 on 2022-08-16 06:24

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220816_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', help_text='Выберите роль пользователя', max_length=9, verbose_name='Пользовательская роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите имя пользователя', max_length=150, unique=True, validators=[users.validators.username_validation], verbose_name='Имя пользователя'),
        ),
    ]