from rest_framework import serializers
from .models import CartModel
from decimal import Decimal

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.product_name")
    customer_name = serializers.ReadOnlyField(source="customer.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = "__all__"
        read_only_fields = ['unit_price', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return round(obj.quantity * obj.unit_price, 2)

    def create(self, validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        unit_price = product.actual_price
        total_price = quantity * unit_price

        validated_data["unit_price"] = unit_price
        validated_data["total_price"] = total_price
        return super().create(validated_data)

   
    