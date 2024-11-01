from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile

# Create your tests here.
class ProfilesModelTests(TestCase):

    def setUp(self):
        # Create a new test user and profile
        self.user = User.objects.create_user(username="testuser", password="Test1234!", email="test.user@mail.utoronto.ca")
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        """ Test that a default unverified profile can be created with the correct fields."""
        # Check for default values
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertFalse(self.profile.is_verified)
        self.assertEqual(self.profile.bio, None)
        self.assertEqual(self.profile.verification_code, None)
        self.assertEqual(self.profile.profilePic, None)
        print("Test: Default Profile Creation - PASS")
    

    def test_profile_str_method(self):
        """ Test that the str method returns the email of the profile passed into it """
        # Verify __str__ returns the user's email
        self.assertEqual(str(self.profile), self.user.email)
        print("Test: Profile __str__ Method - PASS")

    
    def test_generate_verification_code(self):
        """ Test that the generate verification code function works as expected """
        # Generate a verification code
        code = self.profile.generate_verification_code()

        # Check code properties - within range and is numerical
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
        self.assertEqual(self.profile.verification_code, code)
        print("Test: Profile Generate Verification Code Method - PASS")

    
    def test_generate_new_verification_code(self):
        """ Test to ensure a new verification code is generated everytime"""
        old_code = self.profile.verification_code
        new_code = self.profile.generate_verification_code()
        self.assertNotEqual(old_code, new_code)  # ensure the codes are different
        self.assertEqual(self.profile.verification_code, new_code)  # ensure the code has been updated
        print("Test: Generate New Verification Code - PASS")

    
    def test_default_verification_status(self):
        """ Test to ensure the is verified is False by default"""
        self.assertFalse(self.profile.is_verified)
        print("Test: Defaul Verification Status - PASS")


    def test_updated_verification_status(self):
        """ Test to ensure verification status is verified for an user after an update""" 
        # update the verification status for the profile
        self.profile.is_verified = True
        self.profile.save()

        # Check is the verification status for the user's profile is updated
        self.assertTrue(Profile.objects.get(user=self.user).is_verified)
        print("Test: Updated Verification Status - PASS")

    
    




