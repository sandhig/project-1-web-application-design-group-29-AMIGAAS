from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users
from .serializers import UsersSerializer 


@api_view(['POST'])
def add_user(request):
    
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
     
    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

# eventually add delete user 
