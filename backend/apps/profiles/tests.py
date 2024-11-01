from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile
from .serializers import ProfilesSerializer, EmailVerificationSerializer, LoginSerializer
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
        """ Test duplicate profile for same email not allowed"""
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
        """ Test to check that email serializer does not allow for invalid verification code for the given profile"""
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
        """ Test to check that login serializer works as expected"""
        # Define the data to be validated
        data = {'email': self.user_data['email'], 'password' : self.user_data['password'] }

        # Ensure that the user can be successfully logged in
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        print("Test: Successful Login - PASS")


    def test_non_existent_user_login(self):
        """ Test to check that login serializer does not allow login for a non existent user in the database"""
        # Define the data to be validated
        data = {'email': 'nonexistent@example.com', 'password': 'nonexistent'}

        # If user doesn't exists, should trigger errors
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("User not found.", serializer.errors['non_field_errors'][0])
        print("Test: Non-Existent User Login - PASS")
    

    def test_incorrect_credentials(self):
        """ Test to check that login serializer does not allow login for an incorrect email and password pair"""
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





# class ProfileUrlTests(APITestCase):
#     todo = True

# #     def setUp(self):
# #         # Set up a test user for tests that require authentication
# #         self.user = User.objects.create(username="testuser", password="Test1234!")
# #         self.profile = Profile.objects.create(user=self.user)
# #         self.client.login(username="testuser", password="Test1234!")
    
# #     # Tests for add_user endpoint (sign-up)
# #     def test_successfull_signup(self):
# #         """Test that a new user can sign up successfully."""
# #         response = self.client.post(reverse('add_user'), data={
# #             "username": "newtestuser",
# #             "password": "Test12345!",
# #             "email": "newtest.user@mail.utoronto.ca"
# #         })
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #         self.assertIn("username", response.data)
    

# #     def test_signup_missing_fields(self):
# #         """Test that signup fails if required fields are missing."""

# #         # when password is missing
# #         response = self.client.post(reverse('add_user'), data={"username": "newtestuser"})
# #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# #         # when username is missing
# #         response = self.client.post(reverse('add_user'), data={"password": "Test12345!"})
# #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class ProfileViewsTests(TestCase):
#     todo = True



    

