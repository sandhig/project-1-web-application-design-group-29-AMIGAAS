from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image_url = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'category', 'price', 'condition', 'pickup_location', 'description', 'image', 'image_url', 'created_at'] 
