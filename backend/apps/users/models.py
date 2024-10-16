from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string

# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    uoft_email = models.CharField(max_length=255) 
    password = models.CharField(max_length=255, null=True, blank=True)

    def check_user_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.uoft_email 
