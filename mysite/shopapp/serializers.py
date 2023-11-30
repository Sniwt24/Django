from .models import Product, Order
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "pk", "name", "description", "price", "discount", "archived", "created_at"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "pk", "delivery_address", "promocode", "created_at"
