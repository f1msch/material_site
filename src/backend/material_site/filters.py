import django_filters
from .models import Material


class MaterialFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    tags = django_filters.CharFilter(method='filter_tags')
    material_type = django_filters.MultipleChoiceFilter(choices=Material.MATERIAL_TYPES)
    license_type = django_filters.MultipleChoiceFilter(choices=Material.LICENSE_CHOICES)
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')

    class Meta:
        model = Material
        fields = ['category', 'tags', 'material_type', 'license_type',
                  'min_price', 'max_price', 'is_featured']

    def filter_tags(self, queryset, name, value):
        if value:
            tags = value.split(',')
            return queryset.filter(tags__slug__in=tags).distinct()
        return queryset