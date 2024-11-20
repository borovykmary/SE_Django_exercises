from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError

def hello_world(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        if not all([name, price, available is not None]):
            return HttpResponseBadRequest("You have missing fields. Make sure you included all required fields.")

        try:
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201)
    else:
        return HttpResponseBadRequest("Method not allowed")

@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })
    elif request.method == 'POST':
        return HttpResponseBadRequest("The product already exists. Method not allowed")
    else:
        return HttpResponseBadRequest("Method not allowed")