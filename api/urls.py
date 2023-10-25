from django.urls import path
from .views import ProductView, CreateProductView, UserView, LogoutView, LikeView, CartView, MyLikedView

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('createproduct/', CreateProductView.as_view()),
    path('you/', UserView.as_view(), name ='home'),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('like/', LikeView.as_view(), name ='like'),
    path('cart/', CartView.as_view(), name ='cart'),
    path('myliked/', MyLikedView.as_view(), name ='myliked'),
]
