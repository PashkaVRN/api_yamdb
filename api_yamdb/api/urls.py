from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetJWTTokenView, ReviewViewSet, SignUpView, TitleViewSet)

router = routers.DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews_url')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments_url')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')

app_name = 'api'

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('auth/token/', GetJWTTokenView.as_view(), name='get_token')
]
