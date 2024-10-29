from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile

# Create your tests here.
class ProfilesModelTests(TestCase):

    def test_default_profile_creation(self):
        """ Test that a default unverified profile can be created """
        # Create a new test user and profile
        user = User.objects.create_user(username="testuser", password="Test1234!")
        profile = Profile.objects.create(user=user)

        # Check for default values
        self.assertEqual(profile.user, user)
        self.assertFalse(profile.is_verified)
        self.assertIsNone(profile.bio)
        self.assertIsNone(profile.verification_code)
        self.assertEqual(profile.image.name, "default/default-user.jpg")
        print("Test: Default Profile Creation -- PASS")
    

    def test_profile_str_method(self):
        """ Test that the str method returns the email of the profile passed into it"""
        # Create a user with an email
        user = User.objects.create_user(username="testuser", password="Test1234!", email="test.user@mail.utoronto.ca")
        profile = Profile.objects.create(user=user)

        # Verify __str__ returns the user's email
        self.assertEqual(str(profile), user.email)
        print("Test: Profile __str__ Method -- PASS")

    
    
    


