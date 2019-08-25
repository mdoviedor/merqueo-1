from abc import ABC

from pedidos.models import Order, Product, Inventory, Provider, User, OrderProducts
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['address', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'priority', 'user', 'delivery_date', 'products']


class SalesTotalSerializer(serializers.BaseSerializer, ABC):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'total_quantity': obj.total_quantity if obj.total_quantity else 0
        }
