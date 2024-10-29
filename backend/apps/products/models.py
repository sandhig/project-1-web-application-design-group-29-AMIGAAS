from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="")  # Changed default to an empty string
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    condition = models.CharField(max_length=255, default="")  # Changed default to an empty string
    pickup_location = models.CharField(max_length=255, default="")  # Changed default to an empty string
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    edited_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=100, blank=True, null=True)  
    verification_status = models.CharField(
        max_length=20,
        choices=[('verified', 'Verified'), ('unverified', 'Unverified')],
        default='unverified'
    )

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product, blank=True, related_name="wishlisted_by")

    def __str__(self):
        return self.user.username
