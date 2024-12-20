from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Profile
from .serializers import ProfilesSerializer, EmailVerificationSerializer, LoginSerializer
from .views import add_user, verify_email, login_user, get_current_user, list_all_profiles, get_profile, edit_profile, password_reset_request, password_reset_confirm
# from . import views
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
        """ Helper method to create a valid product """
        return Profile.objects.create(**self.valid_profile_data)

    # Testing for valid profile creation
    def test_profile_creation(self):
        """ Test that a valid Product object can be created """
        profile = self.create_valid_profile()
        self.assertIsInstance(profile, Profile)
        print("Test: Valid Profile Creationn - PASS")

    # Test for default fields
    def test_default_verification_status(self):
        """ Test to ensure the is verified is False by default """
        profile = self.create_valid_profile()
        self.assertFalse(profile.is_verified)
        print("Test: Default Verification Status - PASS")

    
    def test_default_bio(self):
        """ Test to ensure the bio is None by default """
        profile = self.create_valid_profile()
        self.assertEqual(profile.bio, None)
        print("Test: Default Bio - PASS")
    

    def test_default_verification_code(self):
        """ Test to ensure the verification code is None by default """
        profile = self.create_valid_profile()
        self.assertEqual(profile.verification_code, None)
        print("Test: Default Verification Code - PASS")


    def test_default_profile_pic_code(self):
        """ Test to ensure the verification code is None by default """
        profile = self.create_valid_profile()
        self.assertEqual(profile.profilePic, None)
        print("Test: Default Profile Pic Code - PASS")


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
        """ Test to ensure a new verification code is generated everytime """
        profile = self.create_valid_profile()
        old_code = profile.verification_code
        new_code = profile.generate_verification_code()
        self.assertNotEqual(old_code, new_code)  # ensure the codes are different
        self.assertEqual(profile.verification_code, new_code)  # ensure the code has been updated
        print("Test: Generate New Verification Code - PASS")

    
    def test_profile_pic_url_without_image(self):
        """ Test profile_pic_url property when no image is uploaded """
        profile = self.create_valid_profile()
        self.assertEqual(profile.profile_pic_url, None)
        print("Test: Profile Pic URL Without Image - PASS")

    
    def test_image_upload_and_profile_pic_url_property(self):
        """ Test the profilePic upload and profile_pic_url property """
        profile = self.create_valid_profile()
        
        # Simulate an image upload
        image_data = SimpleUploadedFile(self.test_image_path, b"file_content", content_type="image/jpeg")
        profile.profilePic = image_data
        profile.save()
        self.assertIsNotNone(profile.profile_pic_url)
        self.assertIn("test_profile_pic.jpg", profile.profile_pic_url)
        print("Test: Image upload Image URL Property - PASS")


    # Updating/Editing Tests
    def test_updated_verification_status(self):
        """ Test to ensure verification status is verified for an user after an update """ 
        # update the verification status for the profile
        profile = self.create_valid_profile()
        profile.is_verified = True
        profile.save()

        # Check is the verification status for the user's profile is updated
        self.assertTrue(Profile.objects.get(user=self.user).is_verified)
        print("Test: Updated Verification Status - PASS")
    

    def test_profile_bio_field(self):
        """ Test setting and retrieving bio field """
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
        print("Test: Bio Max Length - PASS")

    
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


    def test_verification_code_is_null(self):
        """ Test that the profile canhave a blank verification code """
        profile = self.create_valid_profile()
        profile.verification_code = None
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
        """ Test the relationship between user and profile """
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


class ProfilesSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@mail.utoronto.ca',
            'password': 'Test1234!',
            'bio': 'ECE UofT 2T4 + PEY'
        }
        
    
    def test_valid_profile_creation(self):
        """ Test creation with valid data """
        serializer = ProfilesSerializer(data=self.user_data)
        # is_valid = serializer.is_valid()

        # if not is_valid:
        #     print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        profile = serializer.save()
        self.assertIsNotNone(profile.verification_code)  # should be automatically generated and not none
        print("Test: Valid Profile Creation - PASS")

    
    def test_invalid_email_format(self):
        """ Test for invalid email format (must be @mail.utoronto.ca) """
        self.user_data['email'] = 'testuser@example.com'
        serializer = ProfilesSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Please Use UofT Email.", serializer.errors['email'][0])  # Error message should show this
        print("Test: Invalid Email Format - PASS")

    
    def test_duplicate_email(self):
        """ Test duplicate profile for same email not allowed """
        User.objects.create_user(
            username=self.user_data['email'], email=self.user_data['email'], password=self.user_data['password']
        )
        serializer = ProfilesSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Email already exists.", serializer.errors['email'][0])  # Error message should show this
        print("Test: Duplicate Email - PASS")


    def test_update_profile_fields(self):
        """ Test that first name, last name, and bio can be updated, but email cannot e updated """
        # Create a user and profile to test with
        user = User.objects.create_user(username=self.user_data['email'], email=self.user_data['email'], password=self.user_data['password'], first_name=self.user_data['first_name'], last_name=self.user_data['last_name'])
        profile = Profile.objects.create(user=user, bio='Old bio')

        # Define data we want to update
        updated_data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
            'email' : 'newtest.user@mail.utoronto.ca',
            'bio': 'Updated bio'
        }

        # Retain original email
        original_email = user.email

        # Deserialize and update profile, refresh database
        serializer = ProfilesSerializer(instance=profile, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        profile.refresh_from_db()

        # Ensure that first, last name and bio updated, but email did not
        self.assertEqual(user.email, original_email, "Email should not be updated")
        self.assertEqual(profile.user.first_name, 'UpdatedFirstName')
        self.assertEqual(profile.user.last_name, 'UpdatedLastName')
        self.assertEqual(profile.bio, 'Updated bio')
        print("Test: Update Profile Fields - PASS")


    def test_read_only_fields(self):
        """ Test to check that user_id and profilePic_url are read-only """
        serializer = ProfilesSerializer()
        self.assertIn('user_id', serializer.fields)
        self.assertTrue(serializer.fields['user_id'].read_only)
        self.assertIn('profilePic_url', serializer.fields)
        self.assertTrue(serializer.fields['profilePic_url'].read_only)
        print("Test: Read Only Fields - PASS")


class EmailVerificationSerializerTest(TestCase):
    def setUp(self):
        # Create a user, and a profile with a generated verification code
        self.user_data = {
            'email' : 'test.user@mail.utoronto.ca', 
            'password' : 'Test1234!'
        }
        self.user = User.objects.create_user(
            username=self.user_data['email'], email=self.user_data['email'], password=self.user_data['password']
        )
        self.profile = Profile.objects.create(user=self.user)
        self.verification_code = self.profile.generate_verification_code()
    

    def test_non_existent_email(self):
        """ Test to check that email veficiation serializer does not allow for non-existent email in the database """
        # Define the data to be validated
        data = {'email': 'nonexistent@example.com', 'verification_code': '123456'}

        # If email doesn't exist, should trigger error
        serializer = EmailVerificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Email not found.", serializer.errors['non_field_errors'][0])
        print("Test: Non Existent Email - PASS")


    def test_valid_verification_code(self):
        """ Test to check that email serializer works as expected"""
        # Define the data to be validated
        data = {'email': self.user_data['email'], 'verification_code': self.verification_code}

        # Ensure email exists, and verification code is valid, should not trigger error
        serializer = EmailVerificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Update profile and refresh database
        serializer.save()
        self.profile.refresh_from_db()

        # Ensure that the verification codes match and verification status has been updated
        self.assertIsNone(self.profile.verification_code)
        self.assertTrue(self.profile.is_verified)
        print("Test: Valid Verification Code - PASS")

    
    def test_invalid_verification_code(self):
        """ Test to check that email serializer does not allow for invalid verification code for the given profile """
        # Define the data to be validated
        data = {'email': self.user_data['email'], 'verification_code': '654321'}

        # Ensure the data passed in is not the valid verification code
        self.assertNotEqual(data['verification_code'], self.verification_code)

        # Ensure that the verification codes does not match, should trigger error
        serializer = EmailVerificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid verification code.", serializer.errors['non_field_errors'][0])
        print("Test: Invalid Verification Code - PASS")
        

class LoginSerializerTest(TestCase):
    def setUp(self):
        # Create a user, and a profile with a generated verification code
        self.user_data = {
            'email' : 'test.user@mail.utoronto.ca', 
            'password' : 'Test1234!'
        }
        self.user = User.objects.create_user(
            username=self.user_data['email'], email=self.user_data['email'], password=self.user_data['password']
        )
        self.profile = Profile.objects.create(user=self.user, is_verified=True)


    def test_successful_login(self):
        """ Test to check that login serializer works as expected """
        # Define the data to be validated
        data = {'email': self.user_data['email'], 'password' : self.user_data['password'] }

        # Ensure that the user can be successfully logged in
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        print("Test: Successful Login - PASS")


    def test_non_existent_user_login(self):
        """ Test to check that login serializer does not allow login for a non existent user in the database """
        # Define the data to be validated
        data = {'email': 'nonexistent@example.com', 'password': 'nonexistent'}

        # If user doesn't exists, should trigger errors
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("User not found.", serializer.errors['non_field_errors'][0])
        print("Test: Non-Existent User Login - PASS")
    

    def test_incorrect_credentials(self):
        """ Test to check that login serializer does not allow login for an incorrect email and password pair """
        # Define the data to be validated
        wrong_password_data = {'email':  self.user_data['email'], 'password': 'wrongpassword'}
        wrong_email_data = {'email' : 'wrong.email@mail.utorotno.ca', 'password': self.user_data['password']}

        # If password is wrong, it should trigger errors
        serializer = LoginSerializer(data=wrong_password_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Incorrect email or password.", serializer.errors['non_field_errors'][0])

        # If email is wrong, it should trigger errors
        serializer = LoginSerializer(data=wrong_email_data)
        self.assertFalse(serializer.is_valid())
        try: 
            # in the case wrong email exists in the database
            self.assertIn("Incorrect email or password.", serializer.errors['non_field_errors'][0])
        except:
            # in the case wrong email does not exist in the database
            self.assertIn("User not found.", serializer.errors['non_field_errors'][0])
        print("Test: Incorrect Credentials - PASS")


class ProfilesUrlsTests(TestCase):
    def setUp(self):
        # Set up a test user for tests that require authentication
        self.user_email = "test.user@mail.utoronto.ca"
        self.user = User.objects.create_user(username=self.user_email, email=self.user_email, password="Test1234!")
        self.profile = Profile.objects.create(user=self.user, is_verified=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # TODO

    # URL Resolutions
    def test_signup_url_resolves(self):
        """ Test that the 'add_user' URL name resolves to the correct path and view """
        url = reverse('add_user')
        self.assertEqual(resolve(url).func, add_user)
        print('Test: Signup URL Resolves - PASS')
    

    def test_verify_email_url_resolves(self):
        """ Test that 'verify_email' URL name resolves to the correct path and view."""
        url = reverse('verify_email')
        self.assertEqual(resolve(url).func, verify_email)
        print('Test: Verify Email URL Resolves - PASS')
    

    def test_login_url_resolves(self):
        """ Test that the 'login_user' URL name resolves to the correct path and view """
        url = reverse('login_user')
        self.assertEqual(resolve(url).func, login_user)
        print('Test: Login URL Resolves - PASS')
    

    def test_get_user_url_resolves(self):
        """ Test that the 'get_current_user' URL name resolves to the correct path and view """
        url = reverse('get_current_user')
        self.assertEqual(resolve(url).func, get_current_user)
        print('Test: Get User URL Resolves - PASS')

    
    def test_list_all_profiles_url_resolves(self):
        """ Test that the 'list_all_profiles' URL name resolves to the correct path and view """
        url = reverse('list_all_profiles')
        self.assertEqual(resolve(url).func, list_all_profiles)
        print('Test: List All Profiles URL Resolves - PASS')


    def test_get_profile_url_resolves(self):
        """ Test that the 'get-profile' URL name resolves to the correct path and view """
        url = reverse('get-profile', kwargs={'userId': self.profile.user_id})
        self.assertEqual(resolve(url).func, get_profile)
        print('Test: Get Profile URL Resolves - PASS')
    

    def test_edit_profile_url_resolves(self):
        """ Test that the 'edit-profile' URL name resolves to the correct path and view """
        url = reverse('edit-profile')
        self.assertEqual(resolve(url).func, edit_profile)
        print('Test: Edit Profile URL Resolves - PASS')

    
    def test_password_reset_request_url_resolves(self):
        """ Test that the 'password_reset_request' URL name resolves to the correct path and view """
        url = reverse('password_reset_request')
        self.assertEqual(resolve(url).func, password_reset_request)
        print('Test: Password Reset Request URL Resolves - PASS')

    
    def test_password_reset_confirm_url_resolves(self):
        """ Test that the 'password_reset_confirm' URL name resolves to the correct path and view """
        url = reverse('password_reset_confirm')
        self.assertEqual(resolve(url).func, password_reset_confirm)
        print('Test: Password Reset Confirm URL Resolves - PASS')
    

    # Authenticated User Response Tests
    def test_get_user_authenticated_access(self):
        """ Test that authenticated users can access 'get_current_user' """
        response = self.client.get(reverse('get_current_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Test: Authenticated Users can access Get User - PASS')
    

    def test_list_all_profiles_authenticated_access(self):
        """ Test that authenticated users can access 'list_all_profiles' """
        response = self.client.get(reverse('list_all_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Test: Authenticated Users can access List All Profiles - PASS')

    
    def test_get_profile_authenticated_access(self):
        """ Test that authenticated users can access 'get-profile' """
        response = self.client.get(reverse('get-profile', kwargs={'userId': self.profile.user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Test: Authenticated Users can access Get Profile - PASS')

    
    def test_edit_profile_authenticated_access(self):
        """ Test that authenticated users can access 'edit-profile' """
        data = {'bio': 'Updated bio'}
        response = self.client.post(reverse('edit-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('Test: Authenticated Users can access Edit Profile - PASS')

    
    # Authentication Requirement Tests
    def test_get_user_requires_login(self):
        """ Test that unauthenticated users cannot access 'get_current_user' """
        self.client.logout()  # Log out the user
        response = self.client.get(reverse('get_current_user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('Test: Unauthenticated Users cannot access Get User - PASS')
    

    def test_list_all_profiles_requires_login(self):
        """ Test that unauthenticated users cannot access 'list_all_profiles' """
        self.client.logout()  # Log out the user
        response = self.client.get(reverse('list_all_profiles'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('Test: Unauthenticated Users cannot access List All Profiles - PASS')

    
    def test_get_profile_requires_login(self):
        """ Test that unauthenticated users cannot access 'get-profile' """
        self.client.logout()  # Log out the user
        response = self.client.get(reverse('get-profile', kwargs={'userId': self.profile.user_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('Test: Unauthenticated Users cannot access Get Profile - PASS')

    
    def test_edit_profile_requires_login(self):
        """ Test that unauthenticated users cannot access 'edit-profile' """
        self.client.logout()  # Log out the user
        data = {'bio': 'Updated bio'}
        response = self.client.post(reverse('edit-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('Test: Unauthenticated Users cannot access Edit Profile - PASS')
    

class ProfileViewsTests(APITestCase):
    def setUp(self):
        # Set up a test user for tests that require authentication
        self.user_email = "test.user@mail.utoronto.ca"
        self.user_password = "Test1234!"
        self.user = User.objects.create_user(username=self.user_email, email=self.user_email, password=self.user_password)
        self.profile = Profile.objects.create(user=self.user)
        self.profile.is_verified = True
        # self.client = APIClient()

        # Define the endpoint urls
        self.add_user_url = reverse('add_user')
        self.verify_email_url = reverse('verify_email')
        self.login_user_url = reverse('login_user')
        self.get_user_url = reverse('get_current_user')
        self.list_all_url = reverse('list_all_profiles')
        self.get_profile_url = reverse('get-profile', kwargs={'userId': self.profile.user_id})
        self.edit_profile_url = reverse('edit-profile')
        self.password_reset_request_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')
        
        
    # Tests for add_user endpoint (sign-up)
    def test_successfull_signup(self):
        """ Test that a new user can sign up successfully """
        # Define the data to be used
        data = {
            'email' : 'new.test.user@mail.utoronto.ca',
            'password' : 'Test12345!',
            'first_name' : 'New',
            'last_name' : 'User',
            'bio': ''
        }
        
        # send the API request
        response = self.client.post(self.add_user_url, data)

        # Ensure that profile can be signed up / created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User created successfully", response.data['message'])
        print("Test: Successful Signup - PASS")
    

    def test_signup_email_exists(self):
        """ Test that a new user with duplicate email is unsuccessfull """
        # Define the data to be used
        data = {
            'email' : self.user_email,
            'password' : 'Test12345!',
            'first_name' : 'New',
            'last_name' : 'User',
            'bio' : ''
        }

        # send the API request
        response = self.client.post(self.add_user_url, data)

        # Ensure that profile can be signed up / created
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already exists", response.data['error'])
        print("Test: Signup Email Exists - PASS")
    

    def test_signup_missing_fields(self):
        """ Test that signup fails if required fields are missing"""
        valid_data = {
            'email' : 'newmissing.testuser@mail.utoronto.ca',
            'password' : 'Test12345!',
            'first_name' : 'New',
            'last_name' : 'User',
            'bio': ''
        }

        # when password is missing
        invalid_data = valid_data.copy()
        invalid_data.pop('password') # remove the password
        # send the API request
        try:
            response = self.client.post(self.add_user_url, invalid_data)
            self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("Should not be able to create a profile without a password")
        except:
            print("Test: Signup Missing Fields - Password - PASS")
        

        # when email is missing
        invalid_data = valid_data.copy()
        invalid_data.pop('email') # remove the email
        # send the API request
        try:
            response = self.client.post(self.add_user_url, invalid_data)
            self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("Should not be able to create a profile without a password")
        except:
            print("Test: Signup Missing Fields - Email - PASS")

        # when first name is missing
        invalid_data = valid_data.copy()
        invalid_data.pop('first_name') # remove the first_name
        # send the API request
        response = self.client.post(self.add_user_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Signup Missing Fields - First Name - PASS")

        # when last name is missing
        invalid_data = valid_data.copy()
        invalid_data.pop('first_name') # remove the last_name
        # send the API request
        response = self.client.post(self.add_user_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Signup Missing Fields - Last Name - PASS")


    # Tests for verify-email endpoint
    def test_email_verification_valid_code(self):
        """ Test email verification with a valid code """
        # Intentionally set profile's verification status to False
        self.profile.is_verified = False

        # Generate a verification code, ensure the code for the profile is updated
        verification_code = self.profile.generate_verification_code()
        self.assertEqual(self.profile.verification_code, verification_code)

        # send the API request
        data = {'email': self.user.email, 'verification_code': verification_code}
        response = self.client.post(self.verify_email_url, data)

        # Ensure that the email is verified successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Email verified successfully!', response.data['message'])

        # Ensure that profile is verified
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_verified)
        print("Test: Email Verification Valid Code - PASS")

    
    def test_email_verification_invalid_code(self):
        """ Test email verification with an invalid code """
        # Intentionally set profile's verification status to False
        self.profile.is_verified = False

        # Generate a verification code, ensure the code for the profile is updated
        verification_code = self.profile.generate_verification_code()
        self.assertEqual(self.profile.verification_code, verification_code)

        # Define an invalid verification code, ensure they do not match
        invalid_verification_code = "123456"
        if (invalid_verification_code == verification_code): # in the rare occassion this is true
            invalid_verification_code = "654321"
        self.assertNotEqual(self.profile.verification_code, invalid_verification_code)

        # send the API request
        data = {'email': self.user.email, 'verification_code': invalid_verification_code}
        response = self.client.post(self.verify_email_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Email Verification Invalid Code - PASS")
    

    def test_email_verification_missing_code(self):
        """ Test email verification with a missing code """
        # Intentionally set profile's verification status to False
        self.profile.is_verified = False

        # Generate a verification code, ensure the code for the profile is updated
        verification_code = self.profile.generate_verification_code()
        self.assertEqual(self.profile.verification_code, verification_code)

        # send the API request
        data = {'email': self.user.email}
        response = self.client.post(self.verify_email_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Email Verification Missing Code - PASS")


    # Tests for login_user endpoint
    def test_login_valid(self):
        """ Test login with valid credentials """
        # Define the data to be validated
        data = {'email': self.user_email, 'password': self.user_password}
        
        # send the API request
        response = self.client.post(self.login_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Login successful', response.data['message'])
        print("Test: Login Valid - PASS")

    
    def test_login_invalid_password(self):
        """ Test login with incorrect password """
        # Defin the data to be validated
        data = {'email': self.user_email, 'password': 'wrongpassword'}

        # Ensure password is not correct
        self.assertNotEqual(data['password'], self.user_password)

        # send the API request
        response = self.client.post(self.login_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Login Invalid Password - PASS")
    

    def test_login_unverified_user(self):
        """ Test login attempt by unverified user """
        # Create an unverified user profile to test with
        unverified_user = User.objects.create_user(
            username="unverified", email="unverified@mail.utoronto.ca", password="unverifiedpass"
        )
        Profile.objects.create(user=unverified_user, is_verified=False)

        # Define the data to be validated
        data = {'email': 'unverified@mail.com', 'password': 'unverifiedpass'}

        # send the API request
        response = self.client.post(self.login_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Login Unverified User - PASS")


    # Tests for get_current_user endpoint
    def test_get_current_user_authenticated(self):
        """ Test fetching the profile of the authenticated user """
        self.client.force_authenticate(user=self.user)

        # send the API request
        response = self.client.get(self.get_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        print("Test: Get Current User Authenticated - PASS")
    

    def test_get_current_user_unauthenticated(self):
        """ Test accessing current user endpoint without authentication """
        # Send the API request without authenticating
        response = self.client.get(self.get_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Test: Get Current User Unauthenticated - PASS")
    

    # Tests for list_all_profiles endpoint
    def test_list_all_profiles_authenticated(self):
        """ Test listing all profiles as an authenticated user """
        self.client.force_authenticate(user=self.user)  # Login

        # Send the API request
        response = self.client.get(self.list_all_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test: List All Profiles Authenticated - PASS")
    

    def test_list_all_profiles_unauthenticated(self):
        """ Test listing profiles without authentication """
        # Send the API request without authenticating
        response = self.client.get(self.list_all_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Test: List All Profiles Unauthenticated - PASS")

    
    # Tests for get-profile endpoint
    def test_get_profile_valid_user_authenticated(self):
        """ Test fetching a specific user profile by user ID with authentication """
        self.client.force_authenticate(user=self.user)

        # Send the API request
        response = self.client.get(self.get_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['bio'], self.profile.bio)
        self.assertEqual(response.data['profilePic'], self.profile.profilePic)
        print("Test: Get Profile Valid User Authenticated - PASS")
    

    def test_get_profile_valid_user_unauthenticated(self):
        """ Test fetching a specific user profile by user ID with authentication """
        # Send the API request without authentication
        response = self.client.get(self.get_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Test: Get Profile Valid User Unauthenticated - PASS")


    def test_get_profile_invalid_user_authenticated(self):
        """ Test fetching profile with invalid user ID with authentication """
        self.client.force_authenticate(user=self.user)

        # Send the API request without authentication
        url = reverse('get-profile', kwargs={'userId': 99999})  # Assuming 99999 is a non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Get Profile Invalid User Authenticated - PASS")

    
    # Tests for edit-profile endpoint
    def test_edit_profile_valid_data_authenticated(self):
        """ Test editing profile with valid data as an authenticated user """
        self.client.force_authenticate(user=self.user)

        # Send the API request with authentication
        data = {'bio': 'Updated bio content'}
        response = self.client.post(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Refresh the database and ensure it's been updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio content')
        print("Test: Edit Profile Valid Data Authenticated - PASS")

    
    def test_edit_profile_valid_data_unauthenticated_user(self):
        """ Test profile edit attempt by an unauthorized user """
        # Send the API request without authentication
        data = {'bio': 'Unauthorized edit attempt'}
        response = self.client.post(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Test: Edit Profile Valid Data Unauthenticated - PASS")
    

    def test_edit_profile_unauthorized_user(self):
        """ Test profile edit attempt by an unauthorized user, with no profile """
        other_user = User.objects.create_user(username="other.user@mail.utoronto.ca", email="other.user@", password="otherpassword")
        self.client.force_authenticate(user=other_user)

        # send the API request without an authorized profile
        data = {'bio': 'Unauthorized edit attempt'}
        response = self.client.post(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Edit Profile Unauthorized User - PASS")
    

    def test_edit_profile_invalid_data(self):
        """ Test editing profile with invalid data, like trying to change the user's email """
        self.client.force_authenticate(user=self.user)

        # Send the API request with authentication
        data = {'email': 'attempt.update@mail.utoronto.ca'}
        response = self.client.post(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # returns this code but doesn't change anything
        
        # Refresh the database and ensure it hasn't been updated
        self.profile.refresh_from_db()
        self.assertNotEqual(self.user.email, 'attempt.update@mail.utoronto.ca')
        print("Test: Edit Profile Invalid Data - PASS")


    # Tests for password_reset_request endpoint
    def test_password_reset_request_valid_email(self):
        """ Test password reset request with a valid email sends email. """
        with patch('django.core.mail.send_mail') as mock_send_mail:
            # send the API request
            response = self.client.post(self.password_reset_request_url, {'email': self.user.email})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], 'Password reset email sent.')
            mock_send_mail.assert_called_once()  # Confirm email was sent
        print("Test: Password Reset Request Valid Email - PASS")


    def test_password_reset_request_nonexistent_email(self):
        """ Test password reset request with a non-existent email returns 404 status code. """
        # send the API request
        response = self.client.post(self.password_reset_request_url, {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Email not found.')
        print("Test: Password Reset Request Non-Existent Email - PASS")


    def test_password_reset_request_missing_email(self):
        """ Test password reset request without providing email returns 400 status code. """
        # send the API request
        response = self.client.post(self.password_reset_request_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Password Reset Request Missing Email - PASS")
    

    # Tests for password_reset_confirm endpoint
    def test_password_reset_confirm_valid_token_and_uid(self):
        """ Test password reset confirmation with valid token and uid successfully resets password. """
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        new_password = 'newstrongpassword'

        # send the API request
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': uid,
            'token': token,
            'new_password': new_password
        })

        # Ensure that the password has been updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
        print("Test: Password Reset Confirm Valid Token and UID - PASS")


    def test_password_reset_confirm_invalid_token(self):
        """ Test password reset confirmation with an invalid token returns 400 status code. """
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'invalidtoken123'
        new_password = 'newstrongpassword'

        # send the API request
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': uid,
            'token': invalid_token,
            'new_password': new_password
        })

        # Ensure the password hasn't been updated
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token.')
        self.user.refresh_from_db()
        self.assertEqual(self.user_password, self.user.password)
        self.assertNotEqual(new_password, self.user.password)
        print("Test: Password Reset Confirm Invalid Token - PASS")


    def test_password_reset_confirm_invalid_uid(self):
        """ Test password reset confirmation with an invalid uid returns 400 status code. """
        invalid_uid = 'invaliduid123'
        token = default_token_generator.make_token(self.user)
        new_password = 'newstrongpassword'

        # send the API request
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': invalid_uid,
            'token': token,
            'new_password': new_password
        })

        # Ensure the password hasn't been updated
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token or user ID.')
        self.user.refresh_from_db()
        self.assertEqual(self.user_password, self.user.password)
        self.assertNotEqual(new_password, self.user.password)
        print("Test: Password Reset Confirm Invalid UID - PASS")
