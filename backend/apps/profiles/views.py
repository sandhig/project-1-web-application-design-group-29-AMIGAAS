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
from django.shortcuts import get_object_or_404

import boto3
from django.conf import settings

import logging
logger = logging.getLogger('django')


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
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_all_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfilesSerializer(profiles, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile (request, userId):
    profile = get_object_or_404(Profile, user__id=userId)
    serializer = ProfilesSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Unauthorized user
    if request.user.id != profile.user.id:
        return Response({'error': 'You are not authorized to edit this profile.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Serialize profile data
        serializer = ProfilesSerializer(instance=profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # If there is no profile image
            if 'profilePic' not in request.FILES:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            image_file = request.FILES['profilePic']
            filename = image_file.name.replace(" ", "_")
        
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            logger.debug(f's3: {s3}')
            
            image_file.seek(0)
            s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, f'images/{filename}')
            logger.debug('Uploaded')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)