from rest_framework import viewsets

from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateSerializer)

from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (Admin, )
        elif self.request.method == 'DELETE':
            self.permission_classes = (Admin, )
        return super().get_permissions()


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination
    search_fields = ('=name', )
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (Admin, )
        elif self.request.method == 'DELETE':
            self.permission_classes = (Admin, )
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (Admin, )
        elif self.request.method == 'DELETE':
            self.permission_classes = (Admin, )
        return super().get_permissions()
