from django.shortcuts import render
from rest_framework import generics, status
from .models import Product, UserProfile
from .serializers import ProductSerializer, CreateProductSerializer
from .filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import get_object_or_404


# Create your views here.
class ProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CreateProductView(APIView):
    serializer_class = CreateProductSerializer

    def get(self, request):
        print(request.user)
        list = ProductFilter(request.GET, queryset=Product.objects.all())
        products = [{"name": data.name,
                    "brand": data.brand,
                    "slug": data.slug,
                    "condition": data.condition,
                    "user_type": data.user_type,
                    "sold_by": data.sold_by,
                    "prize": data.prize,
                    "product_img": data.product_img.url,  # Assuming product_img is a CloudinaryField
                    "is_liked": 'yes' if request.user in data.liked.all() else 'no',
                    "is_carted": 'yes' if request.user in data.shoppingcarted.all() else 'no',
                    }
                    for data in list.qs]
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


class HomeView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        print(request.user)
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        list = ProductFilter(request.GET, queryset=Product.objects.filter(sold_by=request.user))
        products = [{"name": data.name,
                    "condition": data.condition,
                    "size": data.size,
                    "gender": data.gender,
                    "brand": data.brand,
                    #"slug": data.slug,
                    #"user_type": data.user_type,
                    #"sold_by": data.sold_by,
                    "category": data.category,
                    "prize": data.prize,
                    "product_img": data.product_img.url  # Assuming product_img is a CloudinaryField
                    }
                    for data in list.qs]
        return Response(products)
    

    def post(self, request):
        print(request.data)
        data = request.data
        name = data.get('name')
        print(name)
        condition = data.get('condition')
        print(condition)
        sold_by = request.user
        print(sold_by)
        size = data.get('size')
        print(size)
        gender = data.get('gender')
        print(gender)
        brand = data.get('brand')
        print(brand)
        category = data.get('category')
        print(category)
        prize = 35
        product_img = request.FILES.get('product_img')
        print(product_img)
        product = Product(name=name, condition=condition, sold_by=sold_by,
                           size=size, gender=gender, brand=brand, category=category,
                             prize=prize, product_img=product_img)
        product.save()


        return Response('hej')


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        slug = request.data.get('slug')
        product = get_object_or_404(Product, slug=slug)

        if product.liked.filter(id=request.user.id).exists():
            print('henlo')
            product.liked.remove(request.user)
        else :
            print('babai')
            product.liked.add(request.user)

        print(request.data.get('slug'))
        return Response('liked')
    

class CartView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        slug = request.data.get('slug')
        product = get_object_or_404(Product, slug=slug)

        if product.shoppingcarted.filter(id=request.user.id).exists():
            print('henlo')
            product.shoppingcarted.remove(request.user)
        else :
            print('babai')
            product.shoppingcarted.add(request.user)

        print(request.data.get('slug'))
        return Response('carted')


class MyLikedView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        #queryset = Product.objects.all()

        
        list = ProductFilter(request.GET, queryset=Product.objects.all())
        products = [{"name": data.name,
                    "condition": data.condition,
                    "size": data.size,
                    "gender": data.gender,
                    "brand": data.brand,
                    #"slug": data.slug,
                    #"user_type": data.user_type,
                    #"sold_by": data.sold_by,
                    "category": data.category,
                    "prize": data.prize,
                    "product_img": data.product_img.url  # Assuming product_img is a CloudinaryField
                    }
                    for data in list.qs
                    if request.user in data.liked.all()]
        #print(products)
        return Response(products)

class MyCartView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        #queryset = Product.objects.all()

        
        list = ProductFilter(request.GET, queryset=Product.objects.all())
        products = [{"name": data.name,
                    "condition": data.condition,
                    "size": data.size,
                    "gender": data.gender,
                    "brand": data.brand,
                    #"slug": data.slug,
                    #"user_type": data.user_type,
                    #"sold_by": data.sold_by,
                    "category": data.category,
                    "prize": data.prize,
                    "product_img": data.product_img.url  # Assuming product_img is a CloudinaryField
                    }
                    for data in list.qs
                    if request.user in data.shoppingcarted.all()]
        #print(products)
        return Response(products)

class NewsFeed(APIView):
    def get(self, request):
        feed_products = []
        authent_user = get_object_or_404(UserProfile, username=request.user)

        queryset=Product.objects.all()
        list = UserProfile.objects.all()

        followed_users = authent_user.follows.all()
        for product in queryset:
            for user in followed_users:
                if user.username == product.sold_by:
                    feed_products.append({'name': product.name, 'sold_by': user.username})

        products = [{"username": data.username,
                    }
                    for data in list
                    if request.user in data.follows.all()]

        print('henlo')
        print(products)
        #queryset = Product.objects.all()
        return Response(feed_products)
