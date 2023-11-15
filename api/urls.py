from django.urls import path
from .views import ProductView, CreateProductView, UserView, LogoutView, LikeView, CartView, MyLikedView, MyCartView, NewsFeed

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
]
