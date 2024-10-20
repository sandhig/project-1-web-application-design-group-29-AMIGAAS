from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Profile
from .serializers import ProfilesSerializer, LoginSerializer, EmailVerificationSerializer
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def add_user(request):
    serializer = ProfilesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    # Verify email using EmailVerificationSerializer
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()  # Mark user as verified
        return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        # If valid, return a success message
        return Response({'message': 'Login successful!', 'token': token.key}, status=status.HTTP_200_OK)
    
    # If the data is not valid, return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })
