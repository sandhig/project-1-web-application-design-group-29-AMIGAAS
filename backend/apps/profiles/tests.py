from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile
import os

# Create your tests here.
class ProfilesModelTests(TestCase):

    def setUp(self):
        # Create a new test user and profile
        self.user = User.objects.create_user(username="testuser", password="Test1234!", email="test.user@mail.utoronto.ca")
        self.valid_profile_data = {
            "user" : self.user
        }
        self.test_image_path = os.path.join(os.path.dirname(__file__), 'test_profile_pic.jpg')
        # self.profile = Profile.objects.create(user=self.user)
    
    def create_valid_profile(self):
        """ Helper method to create a valid product"""
        return Profile.objects.create(**self.valid_profile_data)

    # Testing for valid profile creation
    def test_profile_creation(self):
        """ Test that a valid Product object can be created"""
        profile = self.create_valid_profile()
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user, self.user)
        print("Test: Valid Profile Creationn - PASS")

    # Test for default fields
    def test_default_verification_status(self):
        """ Test to ensure the is verified is False by default"""
        profile = self.create_valid_profile()
        self.assertFalse(profile.is_verified)
        print("Test: Default Verification Status - PASS")

    
    def test_default_bio(self):
        """ Test to ensure the bio is None by default"""
        profile = self.create_valid_profile()
        self.assertEqual(profile.bio, None)
        print("Test: Default Bio - PASS")
    

    def test_default_verification_code(self):
        """ Test to ensure the verification code is None by default"""
        profile = self.create_valid_profile()
        self.assertEqual(profile.verification_code, None)
        print("Test: Default Verification Code - PASS")


    def test_default_verification_code(self):
        """ Test to ensure the verification code is None by default"""
        profile = self.create_valid_profile()
        self.assertEqual(profile.verification_code, None)
        print("Test: Default Verification Code - PASS")


    def test_default_profile_pic_code(self):
        """ Test to ensure the verification code is None by default"""
        profile = self.create_valid_profile()
        self.assertEqual(profile.profilePic, None)
        print("Test: Default Verification Code - PASS")


    # Custom Method and Properties Tests
    def test_profile_str_method(self):
        """ Test that the str method returns the email of the profile passed into it """
        profile = self.create_valid_profile()
        # Verify __str__ returns the user's email
        self.assertEqual(str(profile), self.user.email)
        print("Test: Profile __str__ Method - PASS")

    
    def test_generate_verification_code(self):
        """ Test that the generate verification code function works as expected """
        # Generate a verification code
        profile = self.create_valid_profile()
        code = profile.generate_verification_code()

        # Check code properties - within range and is numerical
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
        self.assertEqual(profile.verification_code, code)
        print("Test: Profile Generate Verification Code Method - PASS")

    
    def test_generate_new_verification_code(self):
        """ Test to ensure a new verification code is generated everytime"""
        profile = self.create_valid_profile()
        old_code = profile.verification_code
        new_code = profile.generate_verification_code()
        self.assertNotEqual(old_code, new_code)  # ensure the codes are different
        self.assertEqual(profile.verification_code, new_code)  # ensure the code has been updated
        print("Test: Generate New Verification Code - PASS")

    
    def test_image_url_without_image(self):
        """Test image_url property when no image is uploaded."""
        profile = self.create_valid_profile()
        self.assertEqual(profile.image_url, None)
        print("Test: Image URL Without Image - PASS")

    
    def test_image_upload_and_image_url_property(self):
        """Test the profilePic upload and image_url property."""
        profile = self.create_valid_profile()
        
        # Simulate an image upload
        image_data = SimpleUploadedFile(self.test_image_path, b"file_content", content_type="image/jpeg")
        profile.profilePic = image_data
        profile.save()
        self.assertIsNotNone(profile.image_url)
        print(profile.image_url)
        #self.assertIn("test_image.jpg", self.profile.image_url)
        print("Test: Image upload Image URL Property - PASS")


    # Updating/Editing Tests
    def test_updated_verification_status(self):
        """ Test to ensure verification status is verified for an user after an update""" 
        # update the verification status for the profile
        profile = self.create_valid_profile()
        profile.is_verified = True
        profile.save()

        # Check is the verification status for the user's profile is updated
        self.assertTrue(Profile.objects.get(user=self.user).is_verified)
        print("Test: Updated Verification Status - PASS")
    

    def test_profile_bio_field(self):
        """Test setting and retrieving bio field."""
        profile = self.create_valid_profile()
        test_bio_str = "This is a test bio."
        profile.bio = test_bio_str
        profile.save()

        # Ensure that the bio for this user is updated
        self.assertEqual(Profile.objects.get(user=self.user).bio, test_bio_str)
        print("Test: Profile Bio Field - PASS")

    



