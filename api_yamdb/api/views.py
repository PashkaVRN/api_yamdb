
from random import randint

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .serializers import GetJWTTokenSerializer, SignUpSerializer
from .utils import send_confirmation_code


class SignUpView(APIView):
    """
    Запрос регистрации нового пользователя.
    Создаёт нового пользователя, если он не был создан ранее администратором.
    Отправляет код для подтверждения регистрации на email пользователя.
    """
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')
        if not User.objects.filter(username=username, email=email).exists():
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=username)
        user.confirmation_code = randint(100000, 999999)
        user.save()
        send_confirmation_code(user)
        return Response(serializer.initial_data, status=HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class GetJWTTokenView(APIView):
    """
    Запрос на получение JWT токена.
    Для получения необходим корректный confirmation code.
    """
    def post(self, request):
        serializer = GetJWTTokenSerializer(data=request.data)
        username = serializer.initial_data.get('username')
        user = get_object_or_404(User, username=username)
        if serializer.is_valid():
            return Response(
                {
                    "token": str(
                        RefreshToken.for_user(user)
                    ).access_token
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
