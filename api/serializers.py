from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'shoppingcarted', 'liked',
                  'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'date_added', 'product_img')


