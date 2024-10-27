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
        product = self.create_valid_product()
        self.assertIsNotNone(product.pk)
        print("Test: Valid Product Creation - PASS")
    

    # Testing for invalid object creations (missing fields)
    def test_invalid_product_missing_field_not_allowed(self):
        for field in self.MISSING_FIELDS_NOT_ALLOWED:
            product = self.create_invalid_product_missing_fields(field=field)
            with self.assertRaises(ValidationError):
                product.full_clean()  # Triggers validation
        print("Test: Invalid Product Missing Field Not Allowed - PASS")
    

    def test_inavlid_product_missing_field_allowed(self):
        for field in self.MISSING_FIELDS_ALLOWED:
            result = ""
            try:
                product = self.create_invalid_product_missing_fields(field=field)
                product.full_clean() # should pass without raising validation
                result = "PASS"
            except ValidationError:
                self.fail("full_clean() raised Validation Error unexpectedly")
                result = "FAIl"
        print("Test: Invalid Product Missing Field Allowed - ", result)


    # Max Length Tests 
    def test_name_max_length_within_limit(self):
        product = self.create_valid_product()
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)
        print("Test: Name Max Length Within Limit - PASS")
    

    # Pricing values and decimal tests
    def test_invalid_price_decimals(self):
        product = self.create_invalid_product_inavlid_choice('price', Decimal("12345123456.12"))
        with self.assertRaises(ValidationError):
            product.full_clean() #Triggers validation
        print("Test: Invalid Price Decimals - PASS")


    def test_invalid_price_decimals(self):
        product = self.create_invalid_product_inavlid_choice('price', Decimal("1234.567"))
        with self.assertRaises(ValidationError):
            product.full_clean() #Triggers validation
        print("Test: Invalid Price Decimals - PASS")


    # Invalid Choices Tests
    def test_invalid_category_choice(self):
        product = self.create_invalid_product_inavlid_choice(field='category', invalid_choice="Invalid Category")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test: Invalid Category Choice - PASS")
        
    
    def test_invalid_condition_choice(self):
        product = self.create_invalid_product_inavlid_choice(field='condition', invalid_choice="Invalid Condition")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test: Invalid Condition Choice - PASS")
            

    def test_invalid_pickup_location_choice(self):
        product = self.create_invalid_product_inavlid_choice(field='pickup_location', invalid_choice="Invalid Pick-up Location")
        with self.assertRaises(ValidationError):
            product.full_clean() # Triggers validation
        print("Test : Invalid Pick-up Location Choice - PASS")
    
    # Blank and Null Fields Tests
    def test_description_is_blank(self):
        product = self.create_valid_product()
        product.description = ""
        try: 
            product.full_clean() # Should pass without errors
            print("Test: Description is Blank - PASS")
        except ValidationError:
            self.fail("Product description should allow blank values")
    

    def test_image_is_null(self):
        product = self.create_valid_product()
        product.image = None
        try: 
            product.full_clean() # Should pass without errors
            print("Test: Description is Blank - PASS")
        except ValidationError:
            self.fail("Product image should allow null values")

    
    # Model Relationship Tests
    def test_product_user_relationship(self):
        product = self.create_valid_product()
        self.assertEqual(product.user, self.user)
        print("Test: Product User Relationship - PASS")
    

    def test_product_deletion_on_user_delete(self):
        product = self.create_valid_product()
        self.assertTrue(Product.objects.filter(id=product.id).exists())  # verify product exists in database
        self.user.delete()  # Delete the user
        self.assertFalse(Product.objects.filter(id=product.id).exists(), "Product should be deleted when the user is deleted")
        print('Test: Product Deletion on User Deletion - PASS')


    # Custom Methods and Properties Tests
    def test_product_str_method(self):
        product = self.create_valid_product()
        self.assertEqual(str(product), "Test Valid Product")
        print('Test: Product __str__ Method - PASS')
    
    # TODO add test_image.jpg to AWS S3 bucket
    # def test_image_url_properly_with_image(self):
    #     product = self.create_valid_product()
    #     product.image = 'images/test_image.jpg'
    #     self.assertEqual(product.image_url, '/media/images/test_image.jpg')
    #     print('Test: Image URL Property with Image - PASS')
    
    def test_image_url_property_without_image(self):
        product = self.create_valid_product()
        product.image = None
        self.assertIsNone(product.image_url)
        print('Test: Image URL Property without Image - PASS')


    # Auto generated Date and Time Field Tests
    def test_created_at_auto(self):
        product = self.create_valid_product()
        self.assertIsNotNone(product.created_at)
        print('Test: Created At Automatically Generated - PASS')
    

    def test_edited_at_auto(self):
        product=self.create_valid_product()
        original_edited_at = product.edited_at 
        
        # Update the product to trigger a change in edited_at value
        product.name = "Updated Test Product Name"
        product.save()

        # Verify that edited_at value is updated
        self.assertNotEqual(product.edited_at, original_edited_at)
        print('Test: Edited At Automatically Updated - PASS')

    
    
    