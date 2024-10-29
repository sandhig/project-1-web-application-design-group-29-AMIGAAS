from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from .models import Conversation, Message
from .models import Profile
from . import views

# Create your tests here.
class ConversationModeltests(TestCase):

    # Set up a new Conversation object
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', first_name='Olivia', last_name='Rodrigo', password='Test1234!')
        self.user2 = User.objects.create_user(username='user2', first_name='Sabrina', last_name='Carpenter', password='Test1234!')
        
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
        self.user1 = User.objects.create_user(username='user1', first_name='Olivia', last_name='Rodrigo', password='Test1234!')
        self.user2 = User.objects.create_user(username='user2', first_name='Sabrina', last_name='Carpenter', password='Test1234!')
        
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

class MessagingUrlTests(TestCase):
    # Set up a test client and user to use for authorization where needed
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='Test1234!')
        self.client.force_authenticate(user=self.user)

    # URL Resolution Tests
    def test_get_user_profile_url(self):
        """ Test that the 'get_user_profile/' URL resolves to get_user_profile """
        url = reverse('get_user_profile', args=[1])
        self.assertEqual(url, '/profile/1/')
        self.assertEqual(resolve(url).func, views.get_user_profile)
        print('Test: User Profile URL Resolves - PASS')
    
    def test_get_user_conversations_url(self):
        """ Test that the 'get_user_conversations/' URL resolves to get_user_conversations """
        url = reverse('get_user_conversations')
        self.assertEqual(url, '/conversations/')
        self.assertEqual(resolve(url).func, views.get_user_conversations)
        print('Test: User Conversations URL Resolves - PASS')

    def test_start_conversation_url(self):
        """ Test that the 'start_conversation/' URL resolves to start_conversation """
        url = reverse('start_conversation', args=[1])
        self.assertEqual(url, '/conversation/start/1/')
        self.assertEqual(resolve(url).func, views.start_conversation)
        print('Test: Start Conversation URL Resolves - PASS')

    def test_get_conversation_messages_url(self):
        """ Test that the 'get_conversation_messages/' URL resolves to get_conversation_messages """
        url = reverse('get_conversation_messages', args=[1])
        self.assertEqual(url, '/conversation/1/messages/')
        self.assertEqual(resolve(url).func, views.get_conversation_messages)
        print('Test: Get Conversation Messages URL Resolves - PASS')

    def test_send_message_url(self):
        """ Test that the 'send_message/' URL resolves to send_message """
        url = reverse('send_message')
        self.assertEqual(url, '/send_message/')
        self.assertEqual(resolve(url).func, views.send_message)
        print('Test: Send Message URL Resolves - PASS')

    def test_mark_messages_as_read_url(self):
        """ Test that the 'mark_messages_as_read/' URL resolves to mark_messages_as_read """
        url = reverse('mark_messages_as_read', args=[1])
        self.assertEqual(url, '/conversation/1/mark_as_read/')
        self.assertEqual(resolve(url).func, views.mark_messages_as_read)
        print('Test: Mark Messages As Read URL Resolves - PASS')

    def test_get_unread_messages_url(self):
        """ Test that the 'get_unread_messages/' URL resolves to get_unread_messages """
        url = reverse('get_unread_messages')
        self.assertEqual(url, '/unread_messages/')
        self.assertEqual(resolve(url).func, views.get_unread_messages)
        print('Test: Unread Messages URL Resolves - PASS')

    # Authenticated User Response Tests
    def test_user_profile_authenticated_access(self):
        """ Test that authenticated users can access 'get_user_profile' """
        response = self.client.get(reverse('get_user_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/profile/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        print('Test: Authenticated Users can access User Profile - PASS')
    
    def test_user_conversations_authenticated_access(self):
        """ Test that authenticated users can access 'get_user_conversations' """
        response = self.client.get(reverse('get_user_conversations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/conversations/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can access User Conversations - PASS')
    
    def test_start_conversation_authenticated_access(self):
        """ Test that authenticated users can access 'start_conversation' """
        response = self.client.get(reverse('start_conversation'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/conversation/start/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can start conversations - PASS')

    def test_get_conversation_messages_authenticated_access(self):
        """ Test that authenticated users can access 'get_conversation_messages' """
        response = self.client.get(reverse('get_conversation_messages'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/conversation/1/messages/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can get conversation messages - PASS')

    def test_send_message_authenticated_access(self):
        """ Test that authenticated users can access 'send_message' """
        response = self.client.get(reverse('send_message'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/send_message/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can send messages - PASS')
    
    def test_mark_messages_as_read_authenticated_access(self):
        """ Test that authenticated users can access 'mark_messages_as_read' """
        response = self.client.get(reverse('mark_messages_as_read'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/conversation/1/mark_as_read/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can mark messages as read - PASS')

    def test_get_unread_messages_authenticated_access(self):
        """ Test that authenticated users can access 'get_unread_messages' """
        response = self.client.get(reverse('get_unread_messages'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()  # Log out the user
        response = self.client.get('/unread_messages/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print('Test: Authenticated Users can access unread messages - PASS')
    
#class MessagingViewTests(TestCase):
