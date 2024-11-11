from django.urls import path
from . import views

urlpatterns = [
    path('profiles/signup', views.add_user, name='add_user'),
    path('profiles/verify-email', views.verify_email, name='verify_email'),
    path('profiles/login', views.login_user, name='login_user'),
    path('profiles/get_user', views.get_current_user, name='get_current_user'),
    path('profiles/', views.list_all_profiles, name='list_all_profiles'),
    path('user/<int:userId>/', views.get_profile, name='get-profile'),
    path('profiles/edit-profile/', views.edit_profile, name='edit-profile'),
    path('wishlist/', views.WishlistAPIView.as_view(), name='wishlist'),
    path('wishlist/<int:pk>/', views.WishlistAPIView.as_view(), name='check_wishlist'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]