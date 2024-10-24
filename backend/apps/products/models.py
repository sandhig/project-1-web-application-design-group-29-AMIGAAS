from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Textbook', 'Textbook'),
        ('Clothing', 'Clothing'),
        ('Furniture', 'Furniture'),
        ('Electronics', 'Electronics'),
        ('Stationary', 'Stationary'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Used - Like New'),
        ('Good', 'Used - Good'),
        ('Fair', 'Used - Fair'),
    ]

    LOCATION_CHOICES = [
        ('Robarts', 'Robarts'),
        ('Gerstein', 'Gerstein'),
        ('Computer Science Library', 'Computer Science Library'),
        ('Bahen', 'Bahen'),
        ('Galbraith', 'Galbraith'),
        ('Sanford Fleming', 'Sanford Fleming'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=255, choices=CONDITION_CHOICES)
    pickup_location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        return self.image.url if self.image else None
