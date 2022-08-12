from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатор категории."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатор жанра."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Класс сериализатор получения произведений."""
    genre = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
        many=True
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
        many=False
    )
    
    class Meta:
        fields = '__all__'
        model = Title
    

class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставить только один отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Comment
    

class TitleCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатор создания произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериалайзер рецензий.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Повторный отзыв невозможен')
        return data

    class Meta:
        fields = '__all__'
        model = Review


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
