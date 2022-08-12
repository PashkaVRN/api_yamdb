from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetJWTTokenView, SignUpView, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('auth/token/', GetJWTTokenView.as_view(), name='get_token'),
    path('', include(router.urls))
]
