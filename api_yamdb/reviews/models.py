from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    scope = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    titles = models.ForeignKey(
        Titles,
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

