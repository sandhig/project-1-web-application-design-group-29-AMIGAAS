from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'condition', 'pickup_location', 'description', 'image', 'image_url'] 
