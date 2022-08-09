from django.db import models

from .validators import current_year


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
