from django.urls import path
from . import views

urlpatterns = [
    path('users/signup', views.add_user, name='add_user'),
    path('users/verify-email', views.verify_email, name='verify_email'),
    path('users/login', views.login_user, name='login_user'),
    path('users/get_user', views.get_current_user, name='get_current_user'),
]