from django.urls import path
from .views import OrderView, GetDeliveryLocationView, UpdateDeliveryLocationView

app="orders"

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
    path('orders/<int:order_id>/location/update/', UpdateDeliveryLocationView.as_view(), name='update-location'),
    path('orders/<int:order_id>/location/', GetDeliveryLocationView.as_view(), name='get-location'),
]
