import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Класс, фильтрующий различные поля модели."""

    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='contains')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='contains')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='contains')
    year = django_filters.NumberFilter(field_name='year',
                                       lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
