from django.shortcuts import render
from rest_framework import generics, status
from .models import Product, UserProfile, User
from .serializers import ProductSerializer, CreateProductSerializer, UserProfileSerializer, ProductDetailSerializer, ProductListSerializer
from .filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import get_object_or_404
from django.utils import timezone


# Create your views here.
class ProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

""" class CreateProductView(APIView):
    serializer_class = CreateProductSerializer
    
    def get(self, request):
        print(request.user)
        list = ProductFilter(request.GET, queryset=Product.objects.all())
        products = [{"name": data.name,
                    "brand": data.brand,
                    "slug": data.slug,
                    "condition": data.condition,
                    "user_type": data.user_type,
                    "uploaded_by": data.uploaded_by.username,
                    "profile_slug": get_object_or_404(UserProfile, username=data.uploaded_by).slug,
                    "prize": data.prize,
                    "product_img": data.product_img.url,  # Assuming product_img is a CloudinaryField
                    "is_liked": 'yes' if request.user in data.liked.all() else 'no',
                    "is_carted": 'yes' if request.user in data.shoppingcarted.all() else 'no',
                    }
                    for data in list.qs]
        print(products)
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
            print("Validation errors", serializer.errors) """


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
        print(products)
        return Response(products)
    

    def post(self, request):
        data = request.data
        name = data.get('name')
        condition = data.get('condition')
        uploaded_by = request.user
        size = data.get('size')
        gender = data.get('gender')
        brand = data.get('brand')
        category = data.get('category')
        prize = 35
        product_img = request.FILES.get('product_img')
        product = Product(name=name, condition=condition, uploaded_by=uploaded_by,
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






class NewsFeed(APIView):
    def get(self, request):
        feed_products = []
        authent_user = get_object_or_404(UserProfile, username=request.user)

        queryset=Product.objects.all()
        list = UserProfile.objects.all()

        followed_users = authent_user.follows.all()
        for product in queryset:
            #print(product.uploaded_by)
            for user in followed_users:
                if user == product.uploaded_by:
                    date_added_str = product.date_added.astimezone(timezone.utc).strftime('%Y-%m-%d')
                    
                    feed_products.append({'name': product.name,
                                          'product_img': product.product_img.url,
                                          'profile_pic': get_object_or_404(UserProfile, username=user).profile_pic.url,
                                          'sold_by': user.username,
                                          'profile_slug':  get_object_or_404(UserProfile, username=user).slug,
                                          'uploaded': date_added_str,
                                          'gender': product.gender,
                                          'brand': product.brand,
                                          'prize': product.prize,
                                          'size': product.size,
                                          })

        """ products = [{"username": data.username,
                    }
                    for data in list
                    if request.user in data.follows.all()] """

        print('henlo')
        #print(feed_products)
        #queryset = Product.objects.all()
        return Response(feed_products)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        #slug = request.query_params.get('slug')
        user_profile_username = request.query_params.get('username')
        print(user_profile_username)
        user = get_object_or_404(User, username=user_profile_username)
        print(user)

        profile = get_object_or_404(UserProfile, username=user)
        print(profile)

        # Serialize the profile data using UserProfileSerializer
        serializer = UserProfileSerializer(profile)

        # Return the serialized data as a JSON response
        return Response(serializer.data)
    
class followView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        #Viewed profile
        profile_username = request.data.get('username')
        print(profile_username)
        
        profile = get_object_or_404(User, username=profile_username)
        print(profile)

        #profile_account = get_object_or_404(User, username=profile.username)
        #print(profile_account)

        #Requester
        requester = get_object_or_404(UserProfile, username=request.user)
        print(requester.username)

        if requester.follows.filter(id=profile.id).exists():
            print('works')
            requester.follows.remove(profile)
        else :
            print('dont work')
            requester.follows.add(profile)

        
        return Response('liked')

from rest_framework import status







class UserHome(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        profile = get_object_or_404(UserProfile, username=user)
        # Serialize the profile data using UserProfileSerializer
        serializer = UserProfileSerializer(profile)
        # Return the serialized data as a JSON response
        return Response(serializer.data)


#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   KEEEP

class ProductList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
            print(request.query_params.get('username'))
            user = get_object_or_404(User, username=request.query_params.get('username'))
            print(user)
            profile = get_object_or_404(UserProfile, username=user)

            request_profile = get_object_or_404(UserProfile, username=request.user)
            print(request_profile)
            #user_profile = get_object_or_404(User, username=profile.username)
            product_list = Product.objects.filter(uploaded_by=user)
            
            products = []
            for data in product_list:
                product_data = ProductDetailSerializer(data).data
                is_liked = data.liked.filter(id=request.user.id).exists()
                is_carted = data.shoppingcarted.filter(id=request.user.id).exists()
                is_followed = request_profile.follows.filter(id=user.id).exists()
                product_data['is_liked'] = is_liked
                product_data['is_carted'] = is_carted
                product_data['is_followed'] = is_followed
                products.append(product_data)
            
            return Response(products)
    

class ProductDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print(request.query_params.get('product_slug'))
        product = get_object_or_404(Product, slug=request.query_params.get('product_slug'))
        requester = get_object_or_404(User, username=request.user)
        requester_profile = get_object_or_404(UserProfile, username=requester)
        product_response = ProductDetailSerializer(product).data
        is_followed = requester_profile.follows.filter(id=product.uploaded_by.id).exists()
        is_carted = product.shoppingcarted.filter(id=request.user.id).exists()
        product_response['is_followed'] = is_followed
        product_response['is_carted'] = is_carted
        print(product_response)
        return Response(product_response)
    

class MyCartView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        product_list = Product.objects.all()
        products = []
        for data in product_list:
            if request.user in data.shoppingcarted.all():
                product_data = ProductDetailSerializer(data).data
                is_liked = data.liked.filter(id=request.user.id).exists()
                product_data['is_liked'] = is_liked
                products.append(product_data)
        return Response(products)
    

class MyLikedView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        product_list = Product.objects.all()
        products = []
        for data in product_list:
            if request.user in data.liked.all():
                product_data = ProductDetailSerializer(data).data
                is_liked = data.liked.filter(id=request.user.id).exists()
                product_data['is_liked'] = is_liked
                products.append(product_data)
        return Response(products)
    

class CreateProductView(APIView):
    serializer_class = ProductListSerializer
    
    def get(self, request):
        print(request.user)
        print('newview')
        list = ProductFilter(request.GET, queryset=Product.objects.all())
        products = []
        for data in list.qs:
            product = ProductListSerializer(data).data
            is_liked = data.liked.filter(id=request.user.id).exists()
            product['is_liked'] = is_liked
            products.append(product)
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