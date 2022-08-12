from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetJWTTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', GetJWTTokenView.as_view(), name='get_token')
    path('', include(router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('auth/token/', GetJWTTokenView.as_view(), name='get_token')
]
