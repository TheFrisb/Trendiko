# views.py
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, ProductAttribute
from .serializers import ProductSerializer, ProductAttributeSerializer


class ProductAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)


class ProductAttributeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            product_attribute = ProductAttribute.objects.get(pk=pk)
            serializer = ProductAttributeSerializer(product_attribute)
            return Response(serializer.data)
        except ProductAttribute.DoesNotExist:
            return Response({"error": "Product attribute not found"}, status=404)
