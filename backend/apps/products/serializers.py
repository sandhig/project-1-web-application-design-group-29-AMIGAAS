from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_pic']
    
    def get_profile_pic(self, obj):
        if obj.profile.profile_pic_url:
            return obj.profile.profile_pic_url
        else:
            return None

class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image_url = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'category', 'price', 'condition', 'pickup_location', 'description', 'image', 'image_url', 'created_at', 'sold'] 
