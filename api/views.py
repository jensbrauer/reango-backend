from django.shortcuts import render
from rest_framework import generics, status
from .models import Product
from .serializers import ProductSerializer, CreateProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CreateProductView(APIView):
    serializer_class = CreateProductSerializer

    def get(self, request):
        products = [{"name": data.name,
                    "brand": data.brand}
                    for data in Product.objects.all()]
        return Response(products)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            name = serializer.data.get('name')
            condition = serializer.data.get('condition')
            sold_by = serializer.data.get('sold_by')
            size =  serializer.data.get('size')
            gender =  serializer.data.get('gender')
            brand =  serializer.data.get('brand')
            category =  serializer.data.get('category')
            prize =  serializer.data.get('prize')
            product_img =  serializer.data.get('product_img')

            product = Product(name=name, condition=condition, sold_by=sold_by,
                               size=size, gender=gender, brand=brand, category=category,
                                 prize=prize)
            product.save()

            # Now, save the image associated with the product
            product.product_img = product_img
            product.save()
            return Response(CreateProductSerializer(product).data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors", serializer.errors)


