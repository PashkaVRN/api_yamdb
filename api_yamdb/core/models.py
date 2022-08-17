from django.contrib.auth import get_user_model
from django.db import models

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

