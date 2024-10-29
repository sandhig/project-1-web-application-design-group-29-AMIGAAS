# backend/apps/products/views.py
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product, UserProfile
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# New API endpoint to get wishlist items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist_products = user_profile.wishlist.all()
    serializer = ProductSerializer(wishlist_products, many=True)
    return Response(serializer.data)

# New API endpoint to add a product to the wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    user_profile = UserProfile.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)
    user_profile.wishlist.add(product)
    return Response({"status": "Product added to wishlist"}, status=status.HTTP_200_OK)

# New API endpoint to remove a product from the wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    user_profile = UserProfile.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)
    user_profile.wishlist.remove(product)
    return Response({"status": "Product removed from wishlist"}, status=status.HTTP_200_OK)
