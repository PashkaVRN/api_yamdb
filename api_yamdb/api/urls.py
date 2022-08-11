from django.urls import include, path

from .views import SignUpView, GetJWTTokenView

app_name = 'api'

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('auth/token/', GetJWTTokenView.as_view(), name='get_token')
]
