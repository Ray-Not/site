import django_filters
from .models import Door


class DoorFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Минимальная цена')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Максимальная цена')
    brand = django_filters.CharFilter(method='filter_by_brand', label='Бренд')
    purpose = django_filters.CharFilter(method='filter_by_purpose', label='Назначение')

    class Meta:
        model = Door
        fields = ['price_min', 'price_max', 'brand', 'purpose']

    def filter_by_brand(self, queryset, name, value):
        brands = value.split(',')
        for brand in brands:
            queryset = queryset.filter(title__icontains=brand.strip())
        return queryset

    def filter_by_purpose(self, queryset, name, value):
        purposes = value.split(',')
        print(purposes)
        for purpose in purposes:
            queryset = queryset.filter(purpose__icontains=purpose.strip())
            print(queryset, purpose)
        return queryset
