from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  

    price = models.DecimalField(max_digits=10, decimal_places=2)  

    photo_url = models.URLField(max_length=200)  
    def __str__(self):
        return self.name