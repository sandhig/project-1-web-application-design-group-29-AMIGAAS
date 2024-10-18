from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    uoft_email = models.CharField(max_length=255, unique=True) 
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    # Check the password against the hashed password in the database
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.uoft_email 

    def generate_verification_code(self):
        code = get_random_string(6, '0123456789')
        self.verification_code = code
        self.save()
        return code
