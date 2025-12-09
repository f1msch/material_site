"""
素材过滤器模块
定义Django Filter过滤规则
"""

import django_filters
from django.db.models import QuerySet
from .models import Material


class MaterialFilter(django_filters.FilterSet):
    """
    素材过滤器
    用于API筛选和搜索

    Attributes:
        category: 按分类筛选
        tags: 按标签筛选
        material_type: 按素材类型筛选
        license_type: 按许可类型筛选
        min_price: 最小价格筛选
        max_price: 最大价格筛选
        is_featured: 是否推荐素材
    """

    category = django_filters.CharFilter(
        field_name='category__slug',
        help_text='按分类筛选（slug格式）'
    )

    tags = django_filters.CharFilter(
        method='filter_tags',
        help_text='按标签筛选，多个标签用逗号分隔'
    )

    material_type = django_filters.MultipleChoiceFilter(
        choices=Material.MATERIAL_TYPES,
        help_text='按素材类型筛选'
    )

    license_type = django_filters.MultipleChoiceFilter(
        choices=Material.LICENSE_CHOICES,
        help_text='按许可类型筛选'
    )

    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        help_text='最小价格'
    )

    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        help_text='最大价格'
    )

    is_featured = django_filters.BooleanFilter(
        field_name='is_featured',
        help_text='是否推荐素材'
    )

    search = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text='搜索标题'
    )

    class Meta:
        model = Material
        fields = [
            'category', 'tags', 'material_type', 'license_type',
            'min_price', 'max_price', 'is_featured', 'search'
        ]

    def filter_tags(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        """
        按标签筛选素材

        Args:
            queryset: 原始查询集
            name: 字段名
            value: 标签值，多个用逗号分隔

        Returns:
            QuerySet: 筛选后的查询集
        """
        if value:
            tags = [tag.strip() for tag in value.split(',') if tag.strip()]
            if tags:
                return queryset.filter(tags__slug__in=tags).distinct()
        return queryset