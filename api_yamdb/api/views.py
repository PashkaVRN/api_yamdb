from rest_framework import filters, viewsets, request

from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .filters import TitleFilter
from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateSerializer)

from reviews.models import Category, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = () разрешения
    pagination_class = LimitOffsetPagination


class CategoryViewSet(MixinSet):
    """Класс категория, доступно только админу."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()


class GenreViewSet(MixinSet):
    """Класс жанр, доступно только админу."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()

    permissions.AllowAny


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведения, доступно только админу."""
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

    def get_permissions(self):
        if request.user.is_superuser or request.user.role == 'admin':
            return self.request.method == 'POST' or 'DELETE'
        return super().get_permissions()
