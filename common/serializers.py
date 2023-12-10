from rest_framework import serializers

from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for ProductSerializer"""

        model = Product
        fields = ["id", "title", "regular_price", "sale_price"]
