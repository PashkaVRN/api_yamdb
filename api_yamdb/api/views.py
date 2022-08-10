from rest_framework import viewsets

from rest_framework.pagination import LimitOffsetPagination
from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer)
from .serializers import (CommentSerializer, ReviewSerializer)


from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination

from .mixins import MixinSet
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateSerializer)

from reviews.models import Category, Genre, Review, Title


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
