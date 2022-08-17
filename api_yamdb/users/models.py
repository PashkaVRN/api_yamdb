from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, TextField

from .validators import username_validation


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
    username = CharField(
        unique=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(username_validation,),
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    email = EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты')
    bio = TextField(
        blank=True,
        verbose_name='Биография пользователя',
        help_text='Кратко опишите свою биографию'
    )
    role = CharField(
        max_length=max((len(item) for _, item in ROLE_CHOICES)),
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name='Пользовательская роль',
        help_text='Выберите роль пользователя'
    )
    confirmation_code = CharField(
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
        blank=True
    )

    @property
    def is_moderator(self):
        """True для пользователей с правами модератора."""
        return self.role == User.MODERATOR_ROLE

    @property
    def is_admin(self):
        """True для пользователей с правами админа и суперпользователей."""
        return (
            self.role == User.ADMIN_ROLE
            or self.is_staff
            or self.is_superuser
        )
