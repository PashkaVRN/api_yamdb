from django.urls import include, path
from rest_framework import routers

from .views import (ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews_url')

router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments_url')