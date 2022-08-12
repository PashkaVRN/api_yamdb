from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import filters, viewsets, request
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User
from .permissions import IsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TitleCreateSerializer,
                          UserRestrictedSerializer, UserSerializer)
from .utils import get_confirmation_code, send_confirmation_code
from users.models import User
from .mixins import MixinSet
from .filters import TitleFilter
from .utils import send_confirmation_code
from .permissions import (IsAuthorOrReadOnly, IsAdmin, IsSelf,
                          IsAdminOrReadOnly, IsModeratorAdminOrReadOnly)


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
    permission_classes = [IsAuthorOrReadOnly, IsModeratorAdminOrReadOnly]

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
    permission_classes = [
        IsAuthorOrReadOnly, IsModeratorAdminOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(MixinSet):
    """Класс категория, доступно только админу."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    """Класс жанр, доступно только админу."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведения, доступно только админу."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer
