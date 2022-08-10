from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Review, Comment
from reviews.models import Category, Genre, Title
from rest_framework.serializers import (CharField, EmailField, Serializer,
                                        ValidationError)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
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


class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        model=Comment
    )


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


class SignUpSerializer(Serializer):
    """Сериализатор запроса регистрации нового пользователя."""
    email = EmailField(max_length=254)
    username = CharField(max_length=150)

    def validate_username(self, value):
        """Проверяет, что 'me' не используется как username."""
        if value == 'me':
            raise ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        return value

    def validate_email(self, value):
        """
        Проверяет, что email не используется
        другими зарегестрированными пользователями.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError(
                f'Email {value} уже использется'
            )
        return value


class GetJWTTokenSerializer(Serializer):
    """Сериализатор запроса JWT токена."""
    username = CharField(max_length=150)
    confirmation_code = CharField()
