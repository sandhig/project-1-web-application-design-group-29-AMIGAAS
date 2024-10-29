from django.urls import path
from .views import ProductAPIView, get_product_choices, wishlist_view, add_to_wishlist, remove_from_wishlist
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product_detail'),
    path('product-choices/', get_product_choices, name='get_product_choices'),

    # Wishlist URLs
    path('wishlist/', wishlist_view, name='wishlist-view'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove-from-wishlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

