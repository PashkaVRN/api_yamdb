import re

from rest_framework.serializers import ValidationError


def username_validation(value):
    """
    Нельзя использовать имя пользователя me.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    checked_value = re.match(r'^[\w.@+-]+', value)
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя')
    elif checked_value.group() != value:
        forbidden_simbol = value[checked_value.span()[1]]
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @ . + - _.')
    return value
