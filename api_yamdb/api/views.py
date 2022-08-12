from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, Comment
from users.models import User

from .mixins import MixinSet
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          UserRestrictedSerializer, UserSerializer)
from .utils import get_confirmation_code, send_confirmation_code


class SignUpView(APIView):
    """
    Запрос регистрации нового пользователя.
    Создаёт нового пользователя, если он не был создан ранее администратором.
    Отправляет код для подтверждения регистрации на email пользователя.
    """
    permission_classes = [AllowAny]

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
        user.confirmation_code = get_confirmation_code()
        user.save()
        send_confirmation_code(user)
        return Response(serializer.initial_data, status=HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class GetJWTTokenView(APIView):
    """
    Запрос на получение JWT токена.
    Для получения необходим корректный confirmation code.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetJWTTokenSerializer(data=request.data)
        username = serializer.initial_data.get('username')
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        if not user.confirmation_code == serializer.data['confirmation_code']:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(
            {
                "token": str(
                    RefreshToken.for_user(user).access_token
                )
            }
        )


class UserViewSet(ModelViewSet):
    """
    Вьюсет модели User.
    Администратор имеет полные права доступа.
    Пользователь может просматривать и редактировать свой аккаунт.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False, url_path='me',
        url_name='self_account',
        permission_classes=[IsAuthenticated]
    )
    def self_account(self, request):
        """Просмотр и изменение своего аккаунта."""
        # просмотр
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data,
                status=HTTP_200_OK
            )
        # изменение
        serializer = UserRestrictedSerializer(
            request.user,
            data=request.data,
            partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование рецензий."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnly, IsModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title_id
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        IsAuthorOrReadOnly, IsModeratorAdminOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comment.all()

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


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('=name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer
