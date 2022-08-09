from rest_framework.views import APIView

from .serializers import SignUpSerializer


class SignUpView(APIView):
    """
    Запрос создания нового пользователя.
    Отправка на email кода подтверждения региcтрации.
    """
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

