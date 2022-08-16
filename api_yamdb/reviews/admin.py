from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'title', 'author', 'pub_date',)
    search_fields = ('text', 'author',)
    list_filter = ('pub_date', 'score', 'author', 'title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'review', 'author', 'pub_date',)
    search_fields = ('text', 'author',)
    list_filter = ('pub_date', 'author',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
