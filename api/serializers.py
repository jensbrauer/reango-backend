from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'shoppingcarted', 'liked',
                  'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'date_added', 'product_img')


class CreateProductSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField()
    class Meta:
        model = Product
        fields = ('name', 'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'product_img')