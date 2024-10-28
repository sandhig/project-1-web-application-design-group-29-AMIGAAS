from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('1', 'Category 1'),   
    ('2', 'Category 2'),
    ('3', 'Category 3'),
    ('4', 'Category 4'),
]

CONDITION_CHOICES = [
    ('1', 'New'),
    ('2', 'Used - Like New'),
    ('3', 'Used - Good'),
    ('4', 'Used - Fair'),
]

PICKUP_LOCATION_CHOICES = [     
    ('1', 'Robarts'),
    ('2', 'Gerstein'),
    ('3', 'Computer Science Library'),
    ('4', 'Bahen'),
    ('5', 'Galbraith'),
    ('6', 'Sanford Fleming'),
    ('7', 'Bahen'),
]

class Product(models.Model):
    # required fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='products/') #tentative path, might change later
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=255, choices=CONDITION_CHOICES)
    pickup_location = models.CharField(max_length=255, choices=PICKUP_LOCATION_CHOICES)

    # optional fields
    description = models.TextField(blank=True)
    size = models.CharField(max_length=255, blank=True)
    colour = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
