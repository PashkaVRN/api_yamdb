from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (CommentSerializer, ReviewSerializer, SignUpSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #permission_classes = () разрешения
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = () разрешения

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

class SignUpView(APIView):
    """
    Запрос создания нового пользователя.
    Отправка на email кода подтверждения региcтрации.
    """
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)


