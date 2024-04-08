from rest_framework import serializers

from common.models import MailSubscription
from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for ProductSerializer"""

        model = Product
        fields = ["id", "title", "regular_price", "sale_price"]


class MailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for MailSubscriptionSerializer"""

        model = MailSubscription
        fields = ["email", "created_at"]
