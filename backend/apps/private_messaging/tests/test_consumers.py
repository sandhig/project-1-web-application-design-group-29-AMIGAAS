from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from toogoodtothrow.asgi import application
from unittest.mock import patch
import json
from apps.profiles.models import Profile
from apps.private_messaging.models import Conversation, Message

class ChatConsumerTestCase(TransactionTestCase):
    databases = ['default']

    def setUp(self):
        self.user = Profile.objects.create(id=1, user=get_user_model().objects.create(username="testuser"))
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)

    async def test_connect(self):
        communicator = WebsocketCommunicator(application, f"/ws/chat/user/{self.user.id}/")

        with patch('apps.private_messaging.consumers.ChatConsumer.get_user_conversations') as mock_get_user_conversations:
            mock_get_user_conversations.return_value = [self.conversation]

            connected, _ = await communicator.connect()
            self.assertTrue(connected)

            channel_layer = get_channel_layer()
            await channel_layer.group_add(f'chat_{self.conversation.id}', communicator.channel_name)

            await communicator.disconnect()

