from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'title', 'author', 'pub_date', )
    search_fields = ('text', 'author', )
    list_filter = ('pub_date', 'score', 'author', 'title', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'review', 'author', 'pub_date', )
    search_fields = ('text', 'author', )
    list_filter = ('pub_date', 'author', )


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'get_genre', 'category', )
    search_fields = ('name', )
    list_filter = ('id', )


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    search_fields = ('name', )
    list_filter = ('id', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    search_fields = ('name', )
    list_filter = ('id', )


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
