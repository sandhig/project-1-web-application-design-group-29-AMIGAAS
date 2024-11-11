from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Profile, Wishlist
from .serializers import ProfilesSerializer, LoginSerializer, EmailVerificationSerializer, WishlistSerializer
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..products.models import Product
from ..products.serializers import ProductSerializer
import uuid
import os

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

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
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
        'profile_id': user.profile.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile_pic': Profile.objects.get(user=user).profile_pic_url
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile (request, userId):
    logger.debug(f"GETTING PROFILE {userId}")
    profile = get_object_or_404(Profile, user__id=userId)
    serializer = ProfilesSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_profile(request):

    profile = request.user.profile

    # Unauthorized user
    if request.user.id != profile.user.id:
        return Response({'error': 'You are not authorized to edit this profile.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Serialize profile data
        serializer = ProfilesSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():

            # If there is a profile image
            if 'profilePic' in request.FILES:
                image_file = request.FILES['profilePic']
                image_file.open()
                image_file.read()
                filename = f"{uuid.uuid4().hex}_{os.path.splitext(image_file.name.replace(' ', '_'))[0]}.jpeg"
            
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                image_file.seek(0)
                s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, f'images/{filename}')
                
                logger.debug('Uploaded')
                serializer.save(profilePic=f'images/{filename}')

            else:
                serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class WishlistAPIView(APIView):

    def get(self, request, pk=None):
        current_user = request.user

        if pk:
            # Check if item in wishlist
            product = get_object_or_404(Product, id=pk)
            return Response(Wishlist.objects.select_related('user').filter(product=product, user=current_user).exists())
        else:
            # Return entire wishlist
            wishlist_items = Wishlist.objects.filter(user=current_user).select_related('product')
            products = [item.product for item in wishlist_items]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    # Add to wishlist
    def post(self, request):
        current_user = request.user
        product = get_object_or_404(Product, id=request.data.get("product_id"))

        wishlist_item, created = Wishlist.objects.get_or_create(user=current_user, product=product)

        if not created:
            return Response({"message": "Product already in wishlist."}, status=status.HTTP_200_OK)

        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Remove from Wishlist
    def delete(self, request):
        current_user = request.user
        product = get_object_or_404(Product, id=request.data.get("product_id"))

        try:
            wishlist_item = Wishlist.objects.get(user=current_user, product=product)
            wishlist_item.delete()
            return Response({"message": "Product removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response({"error": "Product not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{settings.FRONTEND_URL}/password_reset_confirm?uid={uid}&token={token}"

    send_mail(
        'Password Reset Request', 
        f'Click the link to reset your password: {reset_url}', 
        'toogoodtothrow59@gmail.com',
        [email], 
        fail_silently = False,
    )

    return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)