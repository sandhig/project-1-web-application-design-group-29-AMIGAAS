from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def validate_email(self, value):
        if '@mail.utoronto.ca' not in value:
            raise serializers.ValidationError("Please Use UofT Email.")

        if Users.objects.filter(uoft_email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return value 
    
    