from rest_framework import serializers
from .models import Users
from django.utils.crypto import get_random_string
import ssl
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password


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
    
    def create(self, validated_data):
        verification_code=get_random_string(length=6, allowed_chars='0123456789')

        user = Users.objects.create (
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            uoft_email=validated_data['uoft_email'],
            verification_code= verification_code,
            is_authenticated=False,
        ) 

        user.set_password(validated_data['password'])  # This hashes the password
        user.save()  # Save the user with the hashed password

        send_mail(
            'Verify Your Email', 
            f'Your verification code is {verification_code}.', 
            'toogoodtothrow59@gmail.com',
            [user.uoft_email], 
            fail_silently = False,
        )
        return user 

class EmailVerificationSerializer(serializers.Serializer):
    uoft_email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        # Check if the email exists
        try:
            user = Users.objects.get(uoft_email=data['uoft_email'])
        except Users.DoesNotExist:
            raise serializers.ValidationError("Email not found.")

        # Check if the verification code matches
        if user.verification_code != data['verification_code']:
            raise serializers.ValidationError("Invalid verification code.")
        
        return data

    def save(self):
        # Mark the user as verified
        uoft_email = self.validated_data['uoft_email']
        user = Users.objects.get(uoft_email=uoft_email)
        user.is_authenticated = True
        user.verification_code = None  # Optionally clear the code after verification
        user.save()


class LoginSerializer(serializers.Serializer) :
    uoft_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        
        try:
            # Fetch the user by email
            user = Users.objects.get(uoft_email=data['uoft_email'])
        except Users.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Check if the email is verified
        if not user.is_authenticated:
            raise serializers.ValidationError("Email is not verified.")

        # Check if the password is correct
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect password.")

        data['user'] = user
        return data
    
    