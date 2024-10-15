from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.get_user_profile, name='get_user_profile'),
    path('conversation/start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/messages/', views.get_conversation_messages, name='get_conversation_messages'),
    path('send_message/', views.send_message, name='send_message'),
]

