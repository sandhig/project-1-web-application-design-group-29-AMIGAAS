from django.urls import path
from .views import ProductAPIView, get_product_choices
from django.conf import settings
from django.conf.urls.static import static
"""
urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.product_list, name='product-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
urlpatterns = [
    path('products/', ProductAPIView.as_view()),
    path('products/<int:pk>/', ProductAPIView.as_view()),
    path('product-choices/', get_product_choices, name='get_product_choices')
]