from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
        self.assertIn("test_profile_pic.jpg", profile.image_url)
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

    # Bio Max Length Tests
    def test_bio_max_length(self):
        """ Test that the maximum length allowed for bio field is correct """
        profile = self.create_valid_profile()
        max_length = profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 500)
        print("Test: Bio Max Length Within Limit - PASS")

    
    def test_bio_max_length_within_limit(self):
        """ Test that a profile can have a bio within maximum limit """
        profile = self.create_valid_profile()
        bio = 'Within Limit Test Bio'
        self.assertLessEqual(len(bio), 255)
        profile.bio = bio
        try:
            profile.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail(f"{bio} should be a within max length limit")
        print('Test: Bio Within Maximum Length')

    
    def test_bio_max_length_over_limit(self):
        """ Test that a profile cannot have a bio over maximum limit """
        profile = self.create_valid_profile()
        bio = 'Long Bio' + ' bio ' * 100
        self.assertLessEqual(255, len(bio))
        with self.assertRaises(ValidationError):
            profile.bio = bio
            profile.full_clean() # Triggers validation
        print("Test: Bio Over Maximum Limit - PASS")
    

    # Verification Code Values
    def test_verification_code_range(self):
        """ Test that the verification code field accepts 6 digits, not more than that """
        """ Code field can be less than 6 digits as per the model, so no testing for that """
        profile = self.create_valid_profile()
        valid_code = '384753'
        invalid_code_big = '12345678'

        # Check that it accepts a code of exactly 6 digits
        self.assertEqual(len(valid_code), 6)
        profile.verification_code = valid_code
        try:
            profile.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail(f"{valid_code} should be accepted")
        print("Test: Verification Code is = 6 digits - PASS")
        
        # Check that it doesn't accept a code of greater than 6 digits
        self.assertGreater(len(invalid_code_big), 6)
        with self.assertRaises(ValidationError):
            profile.verification_code = invalid_code_big
            profile.full_clean() # Triggers validation
        print("Test: Verification Code is > 6 digits - PASS")


    # Blank and Null Fields Tests
    def test_verification_code_is_blank(self):
        """ Test that the profile can have a blank verification code """
        profile = self.create_valid_profile()
        profile.verification_code = ""
        try:
            profile.full_clean()  # Should pass without errors
            print("Test: Verification Code is Blank - PASS")
        except ValidationError:
            self.fail("Profile verificaion model should allow blank values")

    
    def test_bio_is_blank(self):
        """ Test that the profile canhave a blank bio """
        profile = self.create_valid_profile()
        profile.bio = ""
        try:
            profile.full_clean()  # Should pass without errors
            print("Test: Bio is Blank - PASS")
        except ValidationError:
            self.fail("Profile bio should allow blank values")


    def test_verification_code_is_nullk(self):
        """ Test that the profile canhave a blank verification code """
        profile = self.create_valid_profile()
        profile.verification_code = ""
        try:
            profile.full_clean()  # Should pass without errors
            print("Test: Verification Code is Blank - PASS")
        except ValidationError:
            self.fail("Profile verificaion model should allow blank values")


    def test_image_is_null(self):
        """ Test that a profile can have a null image """
        profile = self.create_valid_profile()
        profile.profilePic = None
        try: 
            profile.full_clean() # Should pass without errors
            print("Test: Image is Null - PASS")
        except ValidationError:
            self.fail("Profile image should allow null values")

    
    def test_bio_is_null(self):
        """ Test that a profile can have a null bio """
        profile = self.create_valid_profile()
        profile.bio = None
        try: 
            profile.full_clean() # Should pass without errors
            print("Test: Bio is Null - PASS")
        except ValidationError:
            self.fail("Profile bio should allow null values")

    
    # Model Relationship Tests
    def test_profile_user_relationship(self):
        """ Test the relationship between user and profile"""
        profile = self.create_valid_profile()
        self.assertEqual(profile.user, self.user)
        print("Test: Profile User Relationship - PASS")

    
    def test_profile_deletion_on_user_delete(self):
        """ Test that a profile is deleted when a user is deleted """
        profile = self.create_valid_profile()
        self.assertTrue(Profile.objects.filter(id=profile.id).exists())  # verify profile exists in database
        self.user.delete()  # Delete the user
        self.assertFalse(Profile.objects.filter(id=profile.id).exists(), "Profile should be deleted when the user is deleted")
        print('Test: Profile Deletion on User Deletion - PASS')

    
    # Edge Case Tests
    def test_bio_max_length_boundary(self):
        """ Test that a profile can have a bio at maximum limit """
        profile = self.create_valid_profile()
        profile.name = 'x' * 500
        try:
            profile.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail("Profile bio of 500 characters should be valid")
        print('Test: Edge Case - Bio Boundary - PASS')

    

