from rest_framework import serializers
from .models import Profile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ProfilesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Profile
        fields = ['user_id', 'email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        if '@mail.utoronto.ca' not in value:
            raise serializers.ValidationError("Please Use UofT Email.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return value 
    
    def create(self, validated_data):
        verification_code=get_random_string(length=6, allowed_chars='0123456789')

        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        
        user = User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        user.set_password(password)
        user.save()
        
        profile = Profile.objects.create (
            user=user,
            verification_code=verification_code,
            **validated_data
        ) 

        send_mail(
            'Verify Your Email', 
            f'Your verification code is {verification_code}.', 
            'toogoodtothrow59@gmail.com',
            [profile.user.email], 
            fail_silently = False,
        )
        return profile 

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        # Check if the email exists
        try:
            profile = Profile.objects.get(user__email=data['email'])
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Email not found.")

        # Check if the verification code matches
        if profile.verification_code != data['verification_code']:
            raise serializers.ValidationError("Invalid verification code.")
        
        return data

    def save(self):
        # Mark the user as verified
        email = self.validated_data['email']
        profile = Profile.objects.get(user__email=email)
        profile.is_verified = True
        profile.verification_code = None  # Optionally clear the code after verification
        profile.save()
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        try:
            # Fetch the user by email
            profile = Profile.objects.get(user__email=data['email'])
        except Profile.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        user = authenticate(username=profile.user.username, password=data['password'])
        if user is None:
            raise serializers.ValidationError("Incorrect email or password.")

        data['user'] = user
        return data