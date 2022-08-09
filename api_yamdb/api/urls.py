from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
