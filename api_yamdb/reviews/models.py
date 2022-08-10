from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import current_year

User = get_user_model()

class Category(models.Model):
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
    name = models.TextField(
        'Название',
        max_length=100,
        db_index=True)
    year = models.PositiveIntegerField(
        blank=True,
        validators=[current_year],
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


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    scope = models.IntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, message='Оценка должна быть не больше 10.')
        ],
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    titles = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)
        unique = ('author', 'title')

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата комментария', auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
