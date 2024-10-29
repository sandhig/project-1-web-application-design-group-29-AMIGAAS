from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto3
from django.conf import settings
from .models import Product, Wishlist
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('django')

@api_view(['GET'])
def get_product_choices(request):
    categories = Product.CATEGORY_CHOICES
    conditions = Product.CONDITION_CHOICES
    locations = Product.LOCATION_CHOICES

    # Convert the tuple choices into a more usable format for the frontend
    return Response({
        'categories': [{ 'value': c[0], 'label': c[1] } for c in categories],
        'conditions': [{ 'value': c[0], 'label': c[1] } for c in conditions],
        'locations': [{ 'value': c[0], 'label': c[1] } for c in locations],
    })

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProductAPIView(APIView):
    def get(self, request, pk=None):
        search_term = request.query_params.get('search', None)
        
        if pk:
            product = get_object_or_404(Product, id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.select_related('user').all()
            if search_term:
                products = products.filter(name__icontains=search_term)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)


    def post(self, request):
        logger.debug('Received request for image upload')
        
        try:
            logger.debug(f'Files: {request.FILES}')
            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)

                if 'image' not in request.FILES:
                    logger.debug('Product upload with no image successful')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                image_file = request.FILES['image']
                logger.debug(f'Image file size: {image_file.size} bytes')
            
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                image_file.seek(0)
                s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, f'images/{image_file.name}')

                logger.debug('Image upload successful')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f'Serializer errors: {serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'Error during image upload: {str(e)}')
            return Response({'error': 'Failed to upload image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    products = [item.product for item in wishlist_items]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        return Response({"status": "Product added to wishlist"}, status=status.HTTP_201_CREATED)
    return Response({"status": "Product already in wishlist"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        return Response({"status": "Product removed from wishlist"}, status=status.HTTP_200_OK)
    return Response({"status": "Product not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)