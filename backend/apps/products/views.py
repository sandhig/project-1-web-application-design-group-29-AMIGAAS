from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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
    def get(self, request, key=None):
        if key:
            product = get_object_or_404(Product, key=key)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
