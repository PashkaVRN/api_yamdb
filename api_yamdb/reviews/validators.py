import datetime

from django.core.exceptions import ValidationError


def current_year(year):
    value = datetime.datetime.now().year
    if year > value:
        raise ValidationError(
            'Пожалуйста, укажите правильный год.')
