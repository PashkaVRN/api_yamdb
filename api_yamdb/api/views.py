from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer)
from .serializers import (CommentSerializer, ReviewSerializer, SignUpSerializer)

from reviews.models import Category, Genre, Review, Title



class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    search_fields = ('=name', )
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    search_fields = ('=name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    #permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer



