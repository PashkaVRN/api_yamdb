from django.urls import include, path
from rest_framework import routers

from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet, CategoryViewSet, GenreViewSet, TitleViewSet)

router = routers.DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews_url')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments_url')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
