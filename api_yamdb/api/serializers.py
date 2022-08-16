import datetime as dt

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title

from api_yamdb.settings import (CONFIRMATION_CODE_MAX_LENGTH, EMAIL_MAX_LENGTH,
                                USERNAME_MAX_LENGTH)

from users.validators import username_validation

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
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


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

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Вы уже оставили свой отзыв'
                                                  'к этому произведению!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        """Проверяет корректность имени пользователя."""
        return username_validation(value)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор запроса регистрации нового пользователя."""
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=('Имя уже используется')
            ),
            username_validation
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=('Email уже используется')
            )
        ]
    )


class UserRestrictedSerializer(UserSerializer):
    """
    Сериализатор модели юзер для изменения пользователями своих аккаунтов.
    """
    class Meta(UserSerializer.Meta):
        read_only_fields = ('username', 'email', 'role')


class GetJWTTokenSerializer(serializers.Serializer):
    """Сериализатор запроса JWT токена."""
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=('Имя уже используется')
            ),
            username_validation
        ]
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        required=True
    )
