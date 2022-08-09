from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Review, Title

from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer)


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    search_fields = ['=name', ]
    lookup_field = 'slug'
