from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetJWTTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', GetJWTTokenView.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
