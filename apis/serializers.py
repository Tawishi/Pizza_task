from rest_framework import serializers

from apis.models import Pizza


class OrderPizza(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['type', 'size', 'toppings']
