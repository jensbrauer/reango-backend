from rest_framework import serializers
from .models import Product, UserProfile
from django.shortcuts import get_object_or_404


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'shoppingcarted', 'liked',
                  'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'date_added', 'product_img',
                    'user_type',)


class CreateProductSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField()
    class Meta:
        model = Product
        fields = ('name', 'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'product_img', 'user_type')
        
class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    username = serializers.CharField(source='username.username')

    class Meta:
        model = UserProfile
        fields = ('username', 'description', 'location', 'profile_pic')

    def get_profile_pic(self, obj):
        # Customize the serialization of the 'profile_pic' field
        if obj.profile_pic:
            return obj.profile_pic.url
        else:
            return None
        
class ProductDetailSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField()
    uploaded_by = serializers.CharField(source='uploaded_by.username')
    class Meta:
        model = Product
        fields = ('name', 'slug', 'shoppingcarted', 'liked', 'uploaded_by', 'date_added',
                    'condition', 'sold_by', 'size', 'gender', 'brand',
                    'category', 'prize', 'product_img', 'user_type')

class ProductListSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField()
    uploaded_by = serializers.CharField(source='uploaded_by.username')
    class Meta:
        model = Product
        fields = ('name', 'slug', 'liked', 'uploaded_by', 'date_added',
                    'size', 'prize', 'product_img')
     