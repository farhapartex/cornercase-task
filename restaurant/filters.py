from django_filters import rest_framework as filters
from restaurant.models import Menu


class MenuFilter(filters.FilterSet):
    created_at = filters.DateFilter(method="filter_by_created_at")

    def filter_by_created_at(self, queryset, name, value):
        if value is None:
            return queryset

        return Menu.objects.filter(created_at__date=value)
