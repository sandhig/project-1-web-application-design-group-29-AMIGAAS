from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.get_user_conversations, name='get_user_conversations'),
    path('conversation/start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/messages/', views.get_conversation_messages, name='get_conversation_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/mark_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('unread_messages/', views.get_unread_messages, name='get_unread_messages')
]
