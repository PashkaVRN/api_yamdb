from rest_framework import viewsets, request

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateSerializer)

from reviews.models import Category, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = () разрешения
    pagination_class = LimitOffsetPagination


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
