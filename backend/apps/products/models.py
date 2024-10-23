from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    # required fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='products/') #tentative path, might change later
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)

    # optional fields
    description = models.TextField(blank=True)
    size = models.CharField(max_length=255, blank=True)
    colour = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
