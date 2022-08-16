from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CreatedModel(models.Model):
    """
    Абстрактная модель. Добавляет одинаковые поля моделей Comment и Reviews.
    """
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
