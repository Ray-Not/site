import django_filters
from .models import Door


class DoorFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Минимальная цена'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Максимальная цена'
    )
    brand = django_filters.CharFilter(
        method='filter_by_brand',
        label='Бренд'
    )
    purpose = django_filters.CharFilter(
        method='filter_by_purpose',
        label='Назначение'
    )
    in_cover_name = django_filters.CharFilter(
        method='filter_by_in_cover',
        label='Тип отделки (внутри)'
    )
    out_cover_name = django_filters.CharFilter(
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
            'in_cover_name',
            'out_cover_name',
        ]

    def filter_by_brand(self, queryset, name, value):
        brands = value.split(',')
        for brand in brands:
            queryset = queryset.filter(title__icontains=brand.strip())
        return queryset

    def filter_by_purpose(self, queryset, name, value):
        purposes = value.split(',')
        for purpose in purposes:
            queryset = queryset.filter(purpose__icontains=purpose.strip())
        return queryset

    def filter_by_in_cover(self, queryset, name, value):
        in_covers = value.split(',')
        print(in_covers)
        for in_cover in in_covers:
            queryset = queryset.filter(
                in_cover_name__icontains=in_cover.strip()
            )
            print(queryset)
        return queryset

    def filter_by_out_cover(self, queryset, name, value):
        out_covers = value.split(',')
        print(out_covers)
        for out_cover in out_covers:
            queryset = queryset.filter(
                out_cover_name__icontains=out_cover.strip()
            )
            print(queryset)
        return queryset
