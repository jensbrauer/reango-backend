from django.urls import path
from .views import ProductView, CreateProductView, HomeView, LogoutView

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('createproduct/', CreateProductView.as_view()),
    path('home/', HomeView.as_view(), name ='home'),
    path('logout/', LogoutView.as_view(), name ='logout'),
]
