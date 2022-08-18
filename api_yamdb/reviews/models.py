from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import CommentReviews, Common
from .validator import year_validate

User = get_user_model()


class Category(Common):
    """Модель категорий."""
    pass

    class Meta(Common.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Common):
    """Модель жанров."""
    pass

    class Meta(Common.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель заголовков."""
    name = models.TextField(
        'Название',
        max_length=100,
        db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год',
        blank=True,
        db_index=True,
        validators=(year_validate,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(CommentReviews):
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        default=1,
        validators=[
            MinValueValidator(1, 'Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, 'Оценка должна быть не больше 10.')
        ],
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Название',
    )

    class Meta(CommentReviews.Meta):
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        default_related_name = 'review'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(CommentReviews):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Обзор',
    )

    class Meta(CommentReviews.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
