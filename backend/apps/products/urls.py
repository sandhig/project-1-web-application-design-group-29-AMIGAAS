from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.product_list, name='product-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
