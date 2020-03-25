import django_filters

from quiz.models import Test


class TestFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Test
        fields = ['name']
