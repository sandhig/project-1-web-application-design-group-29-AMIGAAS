from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.create_listing, name='create_listing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
