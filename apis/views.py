# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from . import serializers
from .models import Pizza


@csrf_protect
@api_view(['POST', ])
def create_pizza(request):
    if request.method == 'POST':
        serializer = serializers.OrderPizza(data = request.data)
        if serializer.is_valid():
            pizza_type = request.data.get('type')
            pizza_size = request.data.get('size')
            pizza_toppings = request.data.get('toppings')

            order = Pizza(type = pizza_type, size = pizza_size, toppings = pizza_toppings)
            order.save()
            return Response({'Status': 'Order recorded'}, status = HTTP_200_OK)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


@csrf_protect
@api_view(['GET', ])
def view_pizzas(request):
    if request.method == 'GET':
        record = Pizza.objects.all()
        obj = serializers.OrderPizza(record, many = True)
        return JsonResponse(obj.data, status = HTTP_200_OK, safe = False)


@csrf_protect
@api_view(['POST', ])
def filter_pizzas(request):
    pass


@csrf_protect
@api_view(['PUT', ])
def edit_pizzas():
    pass
