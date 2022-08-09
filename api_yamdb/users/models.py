from django.contrib.auth.models import AbstractUser
from django.db.models import (CharField, CheckConstraint, EmailField, Q,
                              TextField)


class User(AbstractUser):
    """
    Модель пользователя.
    Дополнительные поля биографии и ролей.
    Возможные роли: юзер, модератор, админ.
    Новым пользователям по умолчанию присваивается роль юзер.
    """
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'
    ROLE_CHOICES = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin')
    )
    email = EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты')
    bio = TextField(
        blank=True,
        verbose_name='Биография пользователя',
        help_text='Кратко опишите свою биографию'
    )
    role = CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name='Пользовательская роль',
        help_text='Выберите роль пользователя'
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=(~Q(username='me')),
                name='not_me_username'
            ),
        ]
