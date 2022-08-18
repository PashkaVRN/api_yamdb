from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.settings import LONG

User = get_user_model()


class CommentReviews(models.Model):
    """
    Абстрактная модель. Добавляет одинаковые поля моделей Comment и Reviews.
    """
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta():
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[LONG]


class Common(models.Model):
    name = models.TextField(
        verbose_name='Наименование',
        max_length=100
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
