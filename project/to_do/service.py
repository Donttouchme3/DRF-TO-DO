from django_filters import rest_framework as filters
from .models import Tasks


class TaskFilter(filters.FilterSet):
    start_time = filters.DateFilter(lookup_expr='gte')
    end_time = filters.DateFilter(lookup_expr='lte')

    class Meta:
        model = Tasks
        fields = ('start_time', 'end_time',)
