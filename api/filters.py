import django_filters
from .models import Product, ConditionOPTIONS, SizeOPTIONS, GenderOPTIONS, BrandOPTIONS, CategoryOPTIONS, UserTypeOPTIONS

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'condition', 'size', 'gender', 'brand', 'category', 'user_type', 'sold_by', 'prize']

    condition = django_filters.MultipleChoiceFilter(field_name='condition', choices=ConditionOPTIONS)
    size = django_filters.MultipleChoiceFilter(field_name='size', choices=SizeOPTIONS)
    gender = django_filters.MultipleChoiceFilter(choices=GenderOPTIONS)
    brand = django_filters.MultipleChoiceFilter(choices=BrandOPTIONS)
    category = django_filters.MultipleChoiceFilter(field_name='category', choices=CategoryOPTIONS)
    user_type = django_filters.MultipleChoiceFilter(choices=UserTypeOPTIONS)

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    sold_by = django_filters.CharFilter(field_name='sold_by', lookup_expr='icontains')
    prize_min = django_filters.NumberFilter(field_name='prize', lookup_expr='gte')
    prize_max = django_filters.NumberFilter(field_name='prize', lookup_expr='lte')
