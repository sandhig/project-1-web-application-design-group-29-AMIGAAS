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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_products(request, user_id):
    products = Product.objects.select_related('user').filter(user__id=user_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProductAPIView(APIView):
    def get(self, request, pk=None):
        search_term = request.query_params.get('search', None)
        current_user = request.user.profile
        
        if pk:
            product = get_object_or_404(Product, id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.select_related('user').exclude(user=current_user.user)
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
                filename = image_file.name.replace(" ", "_")
            
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                
                image_file.seek(0)
                s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, f'images/{filename}')

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
