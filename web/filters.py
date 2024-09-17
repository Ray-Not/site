import django_filters
from django.db.models import Q

from .models import Door


class DoorFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='От'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='До'
    )
    brand = django_filters.CharFilter(
        method='filter_by_brand',
        label='Бренд'
    )
    purpose = django_filters.CharFilter(
        method='filter_by_purpose',
        label='Назначение'
    )
    in_covers = django_filters.CharFilter(
        method='filter_by_in_cover',
        label='Тип отделки (внутри)'
    )
    out_covers = django_filters.CharFilter(
        method='filter_by_out_cover',
        label='Тип отделки (снаружи)'
    )

    class Meta:
        model = Door
        fields = [
            'price_min',
            'price_max',
            'brand',
            'purpose',
            'in_covers',
            'out_covers',
        ]

    def filter_by_brand(self, queryset, name, value):
        print(name, value)
        brands = value.split(',')
        query = Q()
        for brand in brands:
            query |= Q(title__icontains=brand.strip())
        return queryset.filter(query)

    def filter_by_purpose(self, queryset, name, value):
        print(name, value)
        purposes = value.split(',')
        query = Q()
        for purpose in purposes:
            query |= Q(purpose__icontains=purpose.strip())
        return queryset.filter(query)

    def filter_by_in_cover(self, queryset, name, value):
        print(name, value)
        in_covers = value.split(',')
        query = Q()
        for in_cover in in_covers:
            query |= Q(in_cover_name__icontains=in_cover.strip())
        return queryset.filter(query)

    def filter_by_out_cover(self, queryset, name, value):
        print(name, value)
        out_covers = value.split(',')
        query = Q()
        for out_cover in out_covers:
            query |= Q(out_cover_name__icontains=out_cover.strip())
        return queryset.filter(query)
