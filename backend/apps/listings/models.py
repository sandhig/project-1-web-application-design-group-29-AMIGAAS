from django.db import models

# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    pickup_location = models.CharField(max_length=100)
    photo = models.URLField()

    def __str__(self):
        return self.name