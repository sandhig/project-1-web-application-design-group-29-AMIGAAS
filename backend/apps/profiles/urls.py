from django.urls import path
from . import views

urlpatterns = [
    path('profiles/signup', views.add_user, name='add_user'),
    path('profiles/verify-email', views.verify_email, name='verify_email'),
    path('profiles/login', views.login_user, name='login_user'),
    path('profiles/get_user', views.get_current_user, name='get_current_user'),
]