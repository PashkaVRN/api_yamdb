import re

from rest_framework.serializers import ValidationError


def username_validation(value):
    """
    Нельзя использовать имя пользователя me.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя')
    elif not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError('Имя пользователя может содержать только буквы, '
                              'цифры и символы @ . + - _.')
    return value