from random import randint

from rest_framework import viewsets, request


from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


from .mixins import MixinSet
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleGetSerializer, TitlePostSerializer)
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование рецензий."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'Admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'Admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'Admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()
        if self.action in ('create', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer