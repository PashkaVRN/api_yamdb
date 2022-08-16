from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title

from users.models import User
from .filters import TitleFilter
from .mixins import MixinSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserRestrictedSerializer, UserSerializer)
from .utils import get_confirmation_code, send_confirmation_code


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
            serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(username=username, email=email)[0]
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

    def post(self, request):
        serializer = GetJWTTokenSerializer(data=request.data)
        username = serializer.initial_data.get('username')
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != serializer.data['confirmation_code']:
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
        serializer = UserRestrictedSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование рецензий."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModeratorAdminOrReadOnly, ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModeratorAdminOrReadOnly, ]

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(MixinSet):
    """Класс категория, доступно только админу."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MixinSet):
    """Класс жанр, доступно только админу."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведения, доступно только админу."""
    queryset = Title.objects.annotate(
        rating=Avg('review__score')).all()
    serializer_class = TitleCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ['name']
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListSerializer
        return TitleCreateSerializer
