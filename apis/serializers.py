from rest_framework import serializers

from apis.models import Pizza


class OrderPizza(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['type', 'size', 'toppings']


class ViewPizza(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'type', 'size', 'toppings']


class FilterPizza(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['type', 'size']
