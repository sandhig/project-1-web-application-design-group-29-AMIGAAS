from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Product



def product_list(request):
    products = Product.objects.all()

    product_data = [{

        "name": product.name,
        "price": product.price,
        "photo_url": product.photo_url

    } for product in products]

    return JsonResponse(product_data, safe=False)


