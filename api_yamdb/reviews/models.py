from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import CreatedModel

User = get_user_model()


class Category(models.Model):
    """Модель категорий."""
    name = models.TextField(
        'Название категории',
        max_length=100)
    slug = models.SlugField(
        'slug',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(
        'Название жанра',
        max_length=50
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель заголовков."""
    name = models.TextField(
        'Название',
        max_length=100,
        db_index=True)
    year = models.PositiveIntegerField(
        blank=True,
        db_index=True
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
        'Описание',
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Review(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
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
        related_name='review',
        verbose_name='Название',
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )
    created = models.DateTimeField(
        'Дата комментария', auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
