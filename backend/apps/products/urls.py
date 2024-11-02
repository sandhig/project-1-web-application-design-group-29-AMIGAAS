from django.urls import path
from .views import ProductAPIView, get_product_choices, get_user_products
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product_detail'),
    path('product-choices/', get_product_choices, name='get_product_choices'),
    path('user-products/<int:user_id>/', get_user_products, name='get_user_products')
]