from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from .models import Conversation, Message

from backend.apps.profiles.models import Profile

# Create your tests here.
class ConversationModeltests(TestCase):

    # Set up a new Conversation object
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', first_name='Olivia', last_name='Rodrigo', password='pass123')
        self.user2 = User.objects.create_user(username='user2', first_name='Sabrina', last_name='Carpenter', password='pass123')
        
        # Create profiles
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        # Add profiles to conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.profile1, self.profile2)
    
    def add_messages(self):
        """ Helper method to add messages to conversation """
        Message.object.create(conversation=self.conversation, sender=self.profile1, content="Hi Sabrina", read=True)
        Message.object.create(conversation=self.conversation, sender=self.profile2, content="Hey Olivia", read=True)
    
    def test_get_other_participant_name(self):
        """ Test the get_other_participant_name method for both users """
        self.assertEqual(self.conversation.get_other_participant_name(self.profile1), "Sabrina Carpenter")
        self.assertEqual(self.conversation.get_other_participant_name(self.profile2), "Olivia Rodrigo")
        print("Test: Get Other Participant Name - PASS")
    
    def test_get_last_message(self):
        """ Test that get_last_message retrieves the last message """
        self.add_messages()
        last_message = self.conversation.get_last_message()
        self.assertEqual(last_message.content, "Hey Olivia")
        self.assertEqual(last_message.sender, self.profile2)
        print("Test: Get Last Message - PASS")
    
    def test_is_read(self):
        """ Test is_read when there are no messages """
        self.assertTrue(self.conversation.is_read(self.profile1))

        """ Test is_read when the last message is from the other user """
        new_message = Message.object.create(conversation=self.conversation, sender=self.profile2, content="What's up?")
        self.assertFalse(self.conversation.is_read(self.profile1))
        new_message.read = True
        new_message.save()
        self.assertTrue(self.conversation.is_read(self.profile1))

        """ Test is_read when the last message is from the current user """
        new_message = Message.object.create(conversation=self.conversation, sender=self.profile1, content="Nothin much")
        self.assertFalse(self.conversation.is_read(self.profile1))
        new_message.read = True
        new_message.save()
        self.assertTrue(self.conversation.is_read(self.profile1))

        print("Test: Check For Unread Messages - PASS")

class MessageModeltests(TestCase):

    # Set up a new Conversation object
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', first_name='Olivia', last_name='Rodrigo', password='pass123')
        self.user2 = User.objects.create_user(username='user2', first_name='Sabrina', last_name='Carpenter', password='pass123')
        
        # Create profiles
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        # Add profiles to conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.profile1, self.profile2)
    
    def test_create_message(self):
        """ Test creation of new message """
        message = Message.objects.create(conversation=self.conversation, sender=self.profile1, content="Test")
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.sender, self.profile1)
        self.assertEqual(message.content, "Test")
        self.assertFalse(message.read)
        print("Test: Check Message Creation - PASS")

    def test_timestamp_auto_creation(self):
        """ Test auto creation of timestamps """
        message = Message.objects.create(conversation=self.conversation, sender=self.profile1, content="Test")
        self.assertIsNotNone(message.timestamp)
        print("Test: Check Timestamp Creation - PASS")

    def test_read_status(self):
        """ Test modification of the read property """
        message = Message.objects.create(conversation=self.conversation, sender=self.profile1, content="Test", read=False)
        self.assertFalse(message.read)
        message.read = True
        message.save()
        self.assertTrue(Message.objects.get(id=message.id).read)
        print("Test: Modify Read Property - PASS")