from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['price_gt', 'price_lt', 'category']
