from django.db import models
from ..users.models import Users

class Product(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
