# backend/apps/products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('wishlist/', views.wishlist_view, name='wishlist-view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
]
