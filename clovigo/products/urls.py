"""
URL mappings for the accounts.
"""
from django.urls import path
from products.views import (ProductGetView,
                            ProductCreate, 
                            ProductGetbyIdView,
                            ProductUpdateView,
                            PostReviewAPIView,
                            ListReviewAPIView,
                            UpdateReviewAPIView,
                            ProductListAPIView)
                            


app_name = "products"

urlpatterns = [

    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path ('productcreate/', ProductCreate.as_view(), name="productcreate"),
    path('productview/<str:product_category>/', ProductGetView.as_view(), name="productget"),
    path('productview/<str:product_name>/', ProductGetbyIdView.as_view(), name='productgetbyname'),
    path('productupdate/<int:id>/', ProductUpdateView.as_view(), name='productupdate'),
    path('reviewpost', PostReviewAPIView.as_view(), name='reviewpost'),
    path('reviewlist/<int:product_id>/', ListReviewAPIView.as_view(), name='reviewlist'),
    path('reviewupdate/<int:pk>/',UpdateReviewAPIView.as_view(), name='reviewupdate'),
   
]
