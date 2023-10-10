import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['condition', 'sold_by', 'size', 'gender', 'brand', 'category']

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    prize_min = django_filters.NumberFilter(field_name='prize', lookup_expr='gte')
    prize_max = django_filters.NumberFilter(field_name='prize', lookup_expr='lte')
