from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from orders.models import OrderModel, DeliveryLocationModel
from cart.models import CartModel
from accounts.models import CustomerModel
from django.contrib.auth.models import AnonymousUser
from .serializers import OrderSerializer, DeliveryLocationSerializer

class OrderView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            customer = CustomerModel.objects.get(user=user)
        except CustomerModel.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            cart_items = CartModel.objects.filter(customer=customer)

            if not cart_items.exists():
                return Response({"error": "Cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

            total_quantity = sum(item.quantity for item in cart_items)
            total_price = sum(float(item.total_price) for item in cart_items)  

            order_data = {
                "customer": customer,
                "quantity": total_quantity,
                "product": [
                    {
                        "product": item.product.product_name,
                        "price": float(item.total_price),
                        "quantity": item.quantity
                    }
                    for item in cart_items
                ],
                "total_price": total_price,
                "order_status": serializer.validated_data.get("order_status", "pending")
            }

            order = OrderModel.objects.create(**order_data)

            #cart_items.delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user

        if isinstance(user, AnonymousUser):
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            customer = CustomerModel.objects.get(user=user)
        except CustomerModel.DoesNotExist:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        orders = OrderModel.objects.filter(customer=customer).order_by("-id")
        
        if not orders.exists():
            return Response({"message": "No orders found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

class UpdateDeliveryLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        location, created = DeliveryLocationModel.objects.get_or_create(order=order)
        location.latitude = request.data.get("latitude")
        location.longitude = request.data.get("longitude")
        location.save()

        return Response({"message": "Location updated successfully."})

class GetDeliveryLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            location = DeliveryLocationModel.objects.get(order__id=order_id)
        except DeliveryLocationModel.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)

        serializer = DeliveryLocationSerializer(location)
        return Response(serializer.data)