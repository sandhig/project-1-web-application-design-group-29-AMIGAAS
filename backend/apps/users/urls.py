from django.urls import path
from . import views

urlpatterns = [
    path('users/signup', views.add_user, name='add_user'),
    path('users/verifyEmail', views.verify_email, name='verify_email'),
    path('users/login', views.login_user, name='login_user')
]