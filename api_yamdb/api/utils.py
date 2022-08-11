from django.core.mail import send_mail


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
        from_email='Vova353@mail.com',
        recipient_list=[user.email]
    )
