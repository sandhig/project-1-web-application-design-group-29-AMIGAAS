import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message, User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    """
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()
    """

    async def connect(self):
        self.conversation_group_names = []
        self.conversations = await self.get_user_conversations(2)

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

        # Save message to database
        message = await self.create_message(self.conversation_id, sender_id, content)

        # Send message to conversation group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender_id': message.sender.id,
                    'sender_name': message.sender.name,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
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
        user = User.objects.get(id=user_id)
        return list(user.conversations.all())

    @database_sync_to_async
    def create_message(self, conversation_id, sender_id, content):
        conversation = Conversation.objects.get(id=conversation_id)
        sender = User.objects.get(id=sender_id)
        message = Message.objects.create(conversation=conversation, sender=sender, content=content)
        return message
