from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

from ..products.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    bio = models.CharField(max_length=500,null=True, blank=True)
    profilePic = models.ImageField(upload_to='images/', null=True, blank=True) 

    def __str__(self):
        return self.user.email

    def generate_verification_code(self):
        code = get_random_string(6, '0123456789')
        self.verification_code = code
        self.save()
        return code
    
    @property
    def profile_pic_url(self):
        return self.profilePic.url if self.profilePic else None

class Wishlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="wishlisted_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'product')

    def __str__(self):
        return f"{self.profile.user.first_name}'s wishlist item: {self.product.name}"
    
