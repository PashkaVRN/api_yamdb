from random import randint

from django.core.mail import send_mail

from api_yamdb.settings import (CONFIRMATION_CODE_MAX_VALUE,
                                CONFIRMATION_CODE_MIN_VALUE,
                                DEFAULT_FROM_EMAIL)


def get_confirmation_code():
    """Генерирует 6-тизначный код."""
    return randint(CONFIRMATION_CODE_MIN_VALUE, CONFIRMATION_CODE_MAX_VALUE)


def send_confirmation_code(user):
    """
    Отправляет код для регистрации на почту.
    В качестве аргумента принимает проверенные данные сериализатора
    и объект пользователя.
    """
    send_mail(
        subject='Регистрация на Yamdb',
        message=(
            'Для завершения регистрации на Yamdb отправьте запрос '
            f'с именем пользователя {user.username} и '
            f'кодом подтверждения {user.confirmation_code} '
            'на эндпойнт /api/v1/auth/token/.'
        ),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
