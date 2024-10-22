import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from apps.profiles.models import Profile
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.conversation_group_names = []
        self.conversations = await self.get_user_conversations(self.user_id)

        for conversation in self.conversations:
            conversation_group_name = f'chat_{conversation.id}'
            self.conversation_group_names.append(conversation_group_name)

            await self.channel_layer.group_add(
                conversation_group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        for conversation_group_name in self.conversation_group_names:
            await self.channel_layer.group_discard(
                conversation_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        sender_id = text_data_json['sender_id']
        conversation_id = text_data_json['conversation_id']

        # Save message to database
        message = await self.create_message(conversation_id, sender_id, content)

        conversation_group_name = f'chat_{conversation_id}'
        sender_first_name = await sync_to_async(lambda: message.sender.user.first_name)()

        # Send message to conversation group
        await self.channel_layer.group_send(
            conversation_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender_id': message.sender.id,
                    'sender_name': sender_first_name,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'conversation_id': conversation_id,
                    'read': message.read
                }
            }
        )

    # Receive message from conversation group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user_conversations(self, user_id):
        user = Profile.objects.prefetch_related(
            'conversations__messages',
            'conversations__participants'
        ).get(id=user_id)
        conversations = user.conversations.all()
        return list(conversations)

    @database_sync_to_async
    def create_message(self, conversation_id, sender_id, content ):
        conversation = Conversation.objects.get(id=conversation_id)
        sender = Profile.objects.get(id=sender_id)
        message = Message.objects.create(conversation=conversation, sender=sender, content=content)
        return message
