from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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


class UserRestrictedSerializer(UserSerializer):
    """
    Сериализатор модели юзер для изменения пользователями своих аккаунтов.

    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class GetJWTTokenSerializer(serializers.Serializer):
    """Сериализатор запроса JWT токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    '''def validate_confirmation_code(self, value):
        """
        Проверяет, что в запросе используется
        корректный код подтверждения.
        """
        username = self.initial_data.get('username')

        if get_object_or_404(
            User,
            username=username
        ).confirmation_code != value:
            raise serializers.ValidationError(
                'Неверный код подтверждения. '
                'Для получения кода подтверждения отправте post запрос '
                'на /api/v1/auth/signup/ c именем пользователя и email.'
            )
        return value'''
