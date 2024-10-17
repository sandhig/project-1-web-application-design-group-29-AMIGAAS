from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users
from .serializers import UsersSerializer, LoginSerializer, EmailVerificationSerializer
from django.core.mail import send_mail

@api_view(['POST'])
def add_user(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_email(request):
    # Verify email using EmailVerificationSerializer
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()  # Mark user as verified
        return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        # If valid, return a success message
        return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
    
    # If the data is not valid, return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
