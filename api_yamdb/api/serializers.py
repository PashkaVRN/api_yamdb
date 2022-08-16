import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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


class TitleListSerializer(serializers.ModelSerializer):
    """Класс сериализатор получения списка произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')
        read_only_fields = ('id', 'author', 'pub_date')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатор создания произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def year_validate(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, 'Оценка должна быть не больше 10.')
        ],
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        request = self.context['request']
        author = request.user
        if (request.method == 'POST'
           and Review.objects.filter(title=title, author=author).exists()):
            raise serializers.ValidationError('Вы уже оставили свой отзыв'
                                              'к этому произведению!')
        return data


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
