from django.db import models

# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    uoft_email = models.CharField(max_length=255) 
    bio = models.TextField()

    def __str__(self):
        return self.first_name 
