from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from products.models import ProductModel,ReviewModel,CustomerModel, CategoryModel
from products.serializers import ProductSerializer,ReviewSerializer, CategorySerializer



class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

class ProductGetView(ListAPIView):
    serializer_class = ProductSerializer
    lookup_field = "product_category"
    def get_queryset(self):
        product_category= self.kwargs.get("product_category")  
        return ProductModel.objects.filter(product_category=product_category)  

class ProductGetbyIdView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "product_name"
    def get_queryset(self):
        product_name= self.kwargs.get("product_name")
        print(product_name)
        return ProductModel.objects.filter(product_name=product_name)

class ProductUpdateView(UpdateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.seller != request.user:
            return Response({"error": "You can only edit your own products."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

class ProductListAPIView(ListAPIView):
    queryset = ProductModel.objects.select_related('seller', 'color_available').order_by('-created_at')
    serializer_class = ProductSerializer


class PostReviewAPIView(CreateAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer

    def context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

class ListReviewAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        product_id = self.kwargs.get("product_id")  
        return ReviewModel.objects.filter(product_id=product_id)   

class UpdateReviewAPIView(UpdateAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    lookup_field ="pk"

    def getobject(self):
        request = self.request
        auth = JWTAuthentication()

        try:
            token = request.headers.get("Authorization").split(" ")[1]
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)

            
            customer = CustomerModel.objects.get(user=user)
            review = super().get_object()
            if review.customer != customer:
                raise PermissionDenied("You are not allowed to update this review.")

            return review

        except CustomerModel.DoesNotExist:
            raise PermissionDenied("No customer account found for this user.")
        except Exception:
            raise PermissionDenied("Invalid or expired token.")


class DjangoFilterBackend:
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can modify categories
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'slug', 'is_active']
    ordering_fields = ['name', 'created_at']
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset