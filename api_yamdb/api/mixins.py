from rest_framework import mixins, viewsets


class MixinSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Класс MixinSet для дальнейшего использования."""
    pass
