from django.urls import path
from .views import ProductView, CreateProductView

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('createproduct/', CreateProductView.as_view()),
]
