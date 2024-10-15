from django.urls import path
from . import views

urlpatterns = [
    path('users/signup', views.add_user, name='add_user'),
    path('users/login', views.login_user, name='login_user')
]