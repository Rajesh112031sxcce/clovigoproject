from rest_framework import serializers
from orders.models import OrderModel, DeliveryLocationModel
from cart.models import CartModel

class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = OrderModel
        fields = "__all__"
        read_only_fields = ['quantity', 'total_price', 'created_at', 'updated_at']

class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocationModel
        fields = ['latitude', 'longitude', 'updated_at']