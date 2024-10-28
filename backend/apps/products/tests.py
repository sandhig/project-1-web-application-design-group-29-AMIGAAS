from django.test import TestCase
from .models import Product
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from .views import ProductAPIView, get_product_choices
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class ProductModeltests(TestCase):
    MISSING_FIELDS_ALLOWED = ['description', 'image']
    MISSING_FIELDS_NOT_ALLOWED = ['user', 'name', 'category', 'price', 'condition', 'pickup_location']
    
    # set up a new product object
    def setUp(self):
        # Create a user for ForeignKey relation
        self.user = User.objects.create(username='testuser', password='Test1234!')
        self.valid_product_data = {
            'user' : self.user,
            'name' : 'Test Valid Product',
            'category' : 'Textbook',
            'price' : Decimal('50.00'),
            'condition' : 'New',
            'pickup_location' : 'Robarts',
            'description' : ' Description for valid test product',
            'image' : ''
        }
    

    def create_valid_product(self):
        """ Helper method to create a valid product"""
        return Product.objects.create(**self.valid_product_data)
    

    def create_invalid_product_missing_fields(self, field):
        """ Helper method to create a product with missing required fields """
        data = self.valid_product_data.copy()
        data.pop(field) # Remove field to simulate a missing field
        return Product(**data) # Avoid changes to skip validation errors
    

    def create_invalid_product_inavlid_choice(self, field, invalid_choice):
        """ Helper method to create a product with invalid choice for a given field """
        data = self.valid_product_data.copy()
        data[field] = invalid_choice 
        return Product(**data) # Avoid changes to skip validation errors
    

    # Testing for valid object creation
    def test_valid_product_creation(self):
        """ Test that a valid product oject can be created """
        product = self.create_valid_product()
        self.assertIsNotNone(product.pk)
        print("Test: Valid Product Creation - PASS")
    

    # Testing for invalid object creations (missing fields)
    def test_invalid_product_missing_field_not_allowed(self):
        """ Test that an inavlid product - missing fields not allowed cannot be created """
        for field in self.MISSING_FIELDS_NOT_ALLOWED:
            product = self.create_invalid_product_missing_fields(field=field)
            with self.assertRaises(ValidationError):
                product.full_clean()  # Triggers validation
        print("Test: Invalid Product Missing Field Not Allowed - PASS")
    

    def test_valid_product_missing_field_allowed(self):
        """ Test that a valid product missing fields allowed can be created"""
        for field in self.MISSING_FIELDS_ALLOWED:
            result = ""
            try:
                product = self.create_invalid_product_missing_fields(field=field)
                product.full_clean() # should pass without raising validation
                result = "PASS"
            except ValidationError:
                self.fail("full_clean() raised Validation Error unexpectedly")
                result = "FAIl"
        print("Test: Valid Product Missing Field Allowed - ", result)


    # Name Max Length Tests 
    def test_name_max_length(self):
        """ Test that the maximum length allowed for name field is correct """
        product = self.create_valid_product()
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)
        print("Test: Name Max Length Within Limit - PASS")
    

    def test_name_max_length_within_limit(self):
        """ Test that a product can have a name within maximum limit """
        product = self.create_valid_product()
        name = 'Within Limit Test Name'
        self.assertLessEqual(len(name), 255)
        product.name = name
        try:
            product.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail(f"{name} should be a within max length limit")
        print('Test: Name Within Maximum Length')
    

    def test_name_max_length_over_limit(self):
        """ Test that a product cannot have a name over maximum limit """
        name = 'Long Input' + 'x' * 255
        self.assertLessEqual(255, len(name))
        product = self.create_invalid_product_inavlid_choice('name', name)
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test: Name Over Maximum Limit - PASS")


    # Pricing values and decimal tests
    def test_invalid_price_range(self):
        """ Test that a product cannot have a price over correct range """
        product = self.create_invalid_product_inavlid_choice('price', Decimal("123456789.10"))
        with self.assertRaises(ValidationError):
            product.full_clean() #Triggers validation
        print("Test: Invalid Price Decimals - PASS")


    def test_invalid_price_decimals(self):
        """ Test that a product cannot have a price with incorrect decimal places"""
        product = self.create_invalid_product_inavlid_choice('price', Decimal("1234.567"))
        with self.assertRaises(ValidationError):
            product.full_clean() #Triggers validation
        print("Test: Invalid Price Decimals - PASS")


    # Invalid Choices Tests
    def test_invalid_category_choice(self):
        """ Test that a product cannot have an incorrect category choice """
        product = self.create_invalid_product_inavlid_choice(field='category', invalid_choice="Invalid Category")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test: Invalid Category Choice - PASS")
        
    
    def test_invalid_condition_choice(self):
        """ Test that a product cannot have an incorrect condition choice """
        product = self.create_invalid_product_inavlid_choice(field='condition', invalid_choice="Invalid Condition")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test: Invalid Condition Choice - PASS")
            

    def test_invalid_pickup_location_choice(self):
        """ Test that a product cannot have an incorrect pickup location choice """
        product = self.create_invalid_product_inavlid_choice(field='pickup_location', invalid_choice="Invalid Pick-up Location")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test : Invalid Pick-up Location Choice - PASS")
    
    # Blank and Null Fields Tests
    def test_description_is_blank(self):
        """ Test that a product can have a blank description """
        product = self.create_valid_product()
        product.description = ""
        try: 
            product.full_clean() # Should pass without errors
            print("Test: Description is Blank - PASS")
        except ValidationError:
            self.fail("Product description should allow blank values")
    

    def test_image_is_null(self):
        """ Test that a product can have a nul image """
        product = self.create_valid_product()
        product.image = None
        try: 
            product.full_clean() # Should pass without errors
            print("Test: Description is Blank - PASS")
        except ValidationError:
            self.fail("Product image should allow null values")

    
    # Model Relationship Tests
    def test_product_user_relationship(self):
        """ Test the relationship between user and product """
        product = self.create_valid_product()
        self.assertEqual(product.user, self.user)
        print("Test: Product User Relationship - PASS")
    

    def test_product_deletion_on_user_delete(self):
        """ Test that a product is deleted when a user is deleted """
        product = self.create_valid_product()
        self.assertTrue(Product.objects.filter(id=product.id).exists())  # verify product exists in database
        self.user.delete()  # Delete the user
        self.assertFalse(Product.objects.filter(id=product.id).exists(), "Product should be deleted when the user is deleted")
        print('Test: Product Deletion on User Deletion - PASS')


    # Custom Methods and Properties Tests
    def test_product_str_method(self):
        """ Test that the str method returns the name of the product """
        product = self.create_valid_product()
        self.assertEqual(str(product), "Test Valid Product")
        print('Test: Product __str__ Method - PASS')
    
    # TODO add test_image.jpg to AWS S3 bucket
    # """ Test that the correct url is returned for the image of a product """
    # def test_image_url_properly_with_image(self):
    #     product = self.create_valid_product()
    #     product.image = 'images/test_image.jpg'
    #     self.assertEqual(product.image_url, '/media/images/test_image.jpg')
    #     print('Test: Image URL Property with Image - PASS')
    
    def test_image_url_property_without_image(self):
        """ Test that a null url is returned for an null image of a product """
        product = self.create_valid_product()
        product.image = None
        self.assertIsNone(product.image_url)
        print('Test: Image URL Property without Image - PASS')


    # Auto generated Date and Time Field Tests
    def test_created_at_auto(self):
        """ Test that the create_at field is automaically generated """
        product = self.create_valid_product()
        self.assertIsNotNone(product.created_at)
        print('Test: Created At Automatically Generated - PASS')
    

    def test_edited_at_auto(self):
        """ Test that the edited_at field is automatically updated """
        product=self.create_valid_product()
        original_edited_at = product.edited_at 
        
        # Update the product to trigger a change in edited_at value
        product.name = "Updated Test Product Name"
        product.save()

        # Verify that edited_at value is updated
        self.assertNotEqual(product.edited_at, original_edited_at)
        print('Test: Edited At Automatically Updated - PASS')
    

    # Database Integrity and Constraint Tests
    def test_valid_category_choices(self):
        """ Test that a product can have a correct category choice """
        product = self.create_valid_product()
        valid_categories = [choice[0] for choice in Product.CATEGORY_CHOICES]
        for category in valid_categories:
            product.category = category
            try:
                product.full_clean()  # Should not raise errors
            except ValidationError:
                self.fail(f"{category} should be a valid choice for category")
        print('Test: Valid Category Choice - PASS')
    

    def test_valid_condition_choices(self):
        """ Test that a product can have a correct condition choice """
        product = self.create_valid_product()
        valid_conditions = [choice[0] for choice in Product.CONDITION_CHOICES]
        for condition in valid_conditions:
            product.condition = condition
            try:
                product.full_clean()  # Should not raise errors
            except ValidationError:
                self.fail(f"{condition} should be a valid choice for condition")
        print('Test: Valid Condition Choice - PASS')

    
    def test_valid_pickup_location_choices(self):
        """ Test that a product can have a correct pickup location choice """
        product = self.create_valid_product()
        valid_locations = [choice[0] for choice in Product.LOCATION_CHOICES]
        for location in valid_locations:
            product.pickup_location = location
            try:
                product.full_clean()  # Should not raise errors
            except ValidationError:
                self.fail(f"{location} should be a valid choice for category")
        print('Test: Valid Location Choice - PASS')

    
    def test_duplicate_product_name_coexists(self):
        """ Test that products with the same name can coexist """
        product = self.create_valid_product()
        duplicate_product = Product(
            user=self.user,
            name=product.name,
            category="Furniture",
            price=Decimal("70.00"),
            condition="Good",
            pickup_location="Bahen"
        )
        duplicate_product.save()
        self.assertEqual(Product.objects.filter(name=product.name).count(), 2)
        print('Test: Duplicate Product Name Coexists - PASS')

    
    # Edge Case Tests
    def test_name_max_length_boundary(self):
        """ Test that a product can have a name at maximum limit """
        product = self.create_valid_product()
        product.name = 'x' * 255
        try:
            product.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail("Product name of 255 characters should be valid")
        print('Test: Edge Case - Name Boundary - PASS')
        
    
    def test_price_boundary_values(self):
        """ Test that a product can have the maximum and minimum range price """
        product = self.create_valid_product()

        # Test minimum price
        product.price = Decimal("0.01")
        try:
            product.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail("Price of 0.01 should be valid")

        # Test maximum price
        product.price = Decimal("99999999.99")
        try:
            product.full_clean()  # Should not raise errors
        except ValidationError:
            self.fail("Price of 99999999.99 should be valid")
        
        print('Test: Edge Case - Price Boundary - PASS')


class ProductUrlTests(TestCase):
    # Set up a test client and user to use for authorization where needed
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='Test1234!')
        self.client.force_authenticate(user=self.user)

        # Create a product to test with
        self.product = Product.objects.create(
            user=self.user,
            name="Test Product",
            category="Textbook",
            price=50.00,
            condition="New",
            pickup_location="Robarts",
            description="Test description",
            image=""
        )
        
    
    # URL Resolution Tests
    def test_product_list_url_resolves(self):
        """ Test that the 'products/' URL resolves to ProductAPIView """
        url = reverse('product_list')
        self.assertEqual(resolve(url).func.view_class, ProductAPIView)
        print('Test: Product List URL Resolves - PASS')


    def test_product_detail_url_resolves(self):
        """ Test that 'products/<int:pk>/' URL resolves to ProductAPIView """
        url = reverse('product_detail', kwargs={'pk' : self.product.id})
        self.assertEqual(resolve(url).func.view_class, ProductAPIView)
        print('Test: Product Detail URL Resolves - PASS')


    def test_product_choices_url_resolves(self):
        """ Test that 'product-choices/' resolves to get_product_choices """
        url = reverse('get_product_choices')
        self.assertEqual(resolve(url).func, get_product_choices)
        print('Test: Product Choices URL Resolves - PASS')


    # Authenticated User Response Tests
    def test_product_list_authenticated_access(self):
        """ Test that authenticated users can access 'product_list' """
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Test: Authenticated Users can access Product List - PASS')


    # # TODO this test produces erors for url, "ProductAPIView.get() got an unexpected keyword argument 'pk'"
    # def test_product_detail_authenticated_access(self):
    #     """ Test that authenticated users can access 'product_detail' """
    #     response = self.client.get(reverse('product_detail', kwargs={'pk' : self.product.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name', self.product.name])
    #     print('Test: Authenticated Users can access Product Detail - PASS')


    def test_product_choices_authenticated_access(self):
        """ Test that authenticated users can access 'get_product_choices' """
        response = self.client.get(reverse('get_product_choices'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('Test: Authenticated Useres can access Product Choices - PASS')
    

    # Authentication Requirement Tests
    def test_product_list_requires_login(self):
        """ Test that unauthenticated users cannot access 'products/' """
        self.client.logout()  # Log out the user
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print('Test: Unauthenticated Users cannot access Product List - PASS')


    def test_product_detail_requires_login(self):
        """ Test that unauthenticated users cannot access 'products/<int:pk>/' """
        self.client.logout()  # Log out the user
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print('Test: Unauthenticated Users cannot access Product Detail- PASS')


    def test_product_choices_requires_login(self):
        """ Test that unauthenticated users cannot access 'product-choices/' """
        self.client.logout()  # Log out the user
        response = self.client.get('/product-choices/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print('Test: Unauthenticated Users cannot access Product Choices - PASS')
