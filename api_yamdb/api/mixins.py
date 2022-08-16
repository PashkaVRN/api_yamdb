from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdminOrReadOnly


class MixinSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    search_fields = ['=name']
    filter_backends = [filters.SearchFilter]
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    """Класс MixinSet для дальнейшего использования."""
    pass
