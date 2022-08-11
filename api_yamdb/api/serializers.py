from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        """Проверяет, что 'me' не используется как username."""
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me в качестве имени пользователя'
            )
        return value


class SignUpSerializer(UserSerializer):
    """Сериализатор запроса регистрации нового пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email')


class GetJWTTokenSerializer(serializers.Serializer):
    """Сериализатор запроса JWT токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate_confirmation_code(self, value):
        """
        Проверяет, что в запросе используется
        корректный код подтверждения.
        """
        username = self.initial_data.get('username')

        if (User.objects.get(
                username=username
        ).confirmation_code != value):
            raise serializers.ValidationError(
                'Неверный код подтверждения. '
                'Для получения кода подтверждения отправте post запрос '
                'на /api/v1/auth/signup/ c именем пользователя и email.'
            )
        return value
