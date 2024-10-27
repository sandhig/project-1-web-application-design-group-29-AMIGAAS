from django.test import TestCase
from .models import Product
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError

# Create your tests here.
class ProductModeltests(TestCase):
    INVALID_LENGTH_INPUT = 'Awsexfcgjhkbcxfghkbvgfgyihbgxfgb hvhcxfgbfgbcguhkbhvchgjvhjlbvguh dfguhjkbhjvhcftuhkhgxdtygihibvcgxf gyhbhvhcfdtyfuygkjbhvghljnbvjghkj cfghbjhgvfcgvkbhjvcgxddygvofhbmb cghkjbmnfcghlcfgchygftyvgujbva Cgvhkjbmvgvhkjbhcfhgyujbvgiggvh jhkjbhcgyhkjbmvghjkhvguhjvhjkm'
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
        self.product = None
        # self.product = Product.objects.create(
        #     user=  self.user,
        #     name = 'Test Valid Product',
        #     category = 'Textbook',
        #     price = Decimal('50.00'),
        #     condition = 'New',
        #     pickup_location = 'Robarts',
        #     description = ' Description for valid test product'
        # )
    
    def create_valid_product(self):
        """ Helper method to create a valid product"""
        return Product.objects.create(**self.valid_product_data)
    
    def create_invalid_product_missing_fields(self, field):
        """ Helper method to create a product with missing required fields """
        data = self.valid_product_data.copy()
        data.pop(field) # Remove field to simulate a missing field
        return Product(**data) # Avoid changes to skip validation errors
    
    # Testing for valid object creation
    def test_valid_product_creation(self):
        product = self.create_valid_product()
        self.assertIsNotNone(product.pk)
        print("Test Case 1 : Test Valid Product Creation - PASS")
    
    # Testing for invalid object creations (missing fields)
    def test_invalid_product_missing_field_not_allowed(self):
        for field in self.MISSING_FIELDS_NOT_ALLOWED:
            print('-- Testing on ', field)
            product = self.create_invalid_product_missing_fields(field=field)
            with self.assertRaises(ValidationError):
                product.full_clean()  # Triggers validation
        print("Test Case 2 : Test Invalid Product Missing Field Not Allowed - PASS")
    
    def test_inavlid_product_missing_field_allowed(self):
        for field in self.MISSING_FIELDS_ALLOWED:
            try:
                product = self.create_invalid_product_missing_fields(field=field)
                product.full_clean() # should pass without raising validation
            except ValidationError:
                self.fail("full_clean() raised Validation Error unexpectedly")
            print("Test Case 3 : Test Invalid Product Missing Field Allowed - PASS")

    # Max Length Tests 
    def test_name_max_length_within_limit(self):
        product = self.create_valid_product()
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, Product.CHAR_MAX_LENGTH)
        print("Test Case 4 : Test Name Max Length Within Limit - PASS")

    # Field Type Tests