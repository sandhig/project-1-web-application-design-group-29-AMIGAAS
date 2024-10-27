from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Add more table columns here!

    def __str__(self):
        return self.name