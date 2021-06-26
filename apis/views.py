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
            try:
                pizza_type = request.data.get('type')
                pizza_size = request.data.get('size').lower()
                pizza_toppings = request.data.get('toppings').lower()

                order = Pizza(type = pizza_type, size = pizza_size, toppings = pizza_toppings)
                order.save()
                return Response({'Status': 'Pizza created'}, status = HTTP_200_OK)
            except Exception:
                return Response({'Status': 'Encountered an error'}, status = HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


@csrf_protect
@api_view(['GET', ])
def view_pizzas(request):
    if request.method == 'GET':
        try:
            record = Pizza.objects.all()
            obj = serializers.ViewPizza(record, many = True)
            return JsonResponse(obj.data, status = HTTP_200_OK, safe = False)
        except Exception:
            return Response({'Status': 'Encountered an error'}, status = HTTP_400_BAD_REQUEST)


@csrf_protect
@api_view(['POST', ])
def filter_pizzas(request):
    if request.method == 'POST':
        serializer = serializers.FilterPizza(data = request.data)
        if serializer.is_valid():
            try:
                pizza_type = request.data.get('type')
                pizza_size = request.data.get('size').lower()

                data = Pizza.objects.filter(type = pizza_type, size = pizza_size)
                obj = serializers.ViewPizza(data, many = True)
                return JsonResponse(obj.data, status = HTTP_200_OK, safe = False)
            except Exception:
                return Response({'Status': 'Encountered an error'}, status = HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


@csrf_protect
@api_view(['DELETE', ])
def delete_pizzas(request):
    if request.method == 'DELETE':
        try:
            pizza_id = request.data.get('id')
            if pizza_id == '' or (not Pizza.objects.filter(id = pizza_id).exists()):
                return JsonResponse({'id': 'Please enter valid id'}, status = HTTP_400_BAD_REQUEST, safe = False)
            Pizza.objects.get(id = int(pizza_id)).delete()
            return JsonResponse({'Status': 'Pizza entry deleted'}, status = HTTP_200_OK, safe = False)
        except Exception:
            return Response({'Status': 'Encountered an error'}, status = HTTP_400_BAD_REQUEST)


@csrf_protect
@api_view(['PUT', ])
def edit_pizzas(request):
    if request.method == 'PUT':
        try:
            pizza_id = request.data.get('id')
            if pizza_id == '' or (not Pizza.objects.filter(id = pizza_id).exists()):
                return JsonResponse({'id': 'Please enter valid id'}, status = HTTP_400_BAD_REQUEST, safe = False)

            pizza_type = request.data.get('type')
            pizza_size = request.data.get('size')
            pizza_toppings = request.data.get('toppings')

            if pizza_size is None:
                return JsonResponse({'size': 'Required'}, status = HTTP_400_BAD_REQUEST, safe = False)

            if pizza_type is None:
                return JsonResponse({'type': 'Required'}, status = HTTP_400_BAD_REQUEST, safe = False)

            new_type = Pizza.objects.get(id = pizza_id).type
            new_size = Pizza.objects.get(id = pizza_id).size.lower()
            if pizza_toppings is None:
                new_toppings = Pizza.objects.get(id = pizza_id).toppings
            else:
                new_toppings = Pizza.objects.get(id = pizza_id).toppings + pizza_toppings

            if pizza_type != '':
                new_type = pizza_type

            if pizza_size != '':
                new_size = pizza_size

            Pizza.objects.filter(id = pizza_id).update(type = new_type, size = new_size, toppings = new_toppings)
            return Response({'Status': 'Pizza edited'}, status = HTTP_200_OK)
        except Exception:
            return Response({'Status': 'Encountered an error'}, status = HTTP_400_BAD_REQUEST)
