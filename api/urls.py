from django.urls import path
from .views import ProductDetails, ProductView, CreateProductView, UserView, LogoutView, LikeView, CartView, MyLikedView, MyCartView, NewsFeed, ProfileView, followView, ProductList, UserHome

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('createproduct/', CreateProductView.as_view()),
    path('you/', UserView.as_view(), name ='home'),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('like/', LikeView.as_view(), name ='like'),
    path('cart/', CartView.as_view(), name ='cart'),
    path('myliked/', MyLikedView.as_view(), name ='myliked'),
    path('mycart/', MyCartView.as_view(), name ='mycart'),
    path('news/', NewsFeed.as_view(), name ='news'),
    path('profile/', ProfileView.as_view(), name ='profile'),
    path('follow/', followView.as_view(), name ='follow'),
    path('product_list/', ProductList.as_view(), name ='product_list'),
    path('user_home/', UserHome.as_view(), name ='user_home'),
    path('product_details/', ProductDetails.as_view(), name ='product_details'),
]
