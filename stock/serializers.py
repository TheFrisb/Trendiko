from enum import Enum

from rest_framework import serializers

from shop.models import Product
from stock.models import StockItem


class AvailableStockManagerActions(Enum):
    ADD_QUANTITY = "ADD"
    REMOVE_QUANTITY = "REMOVE"


class ManageStockItemSerializer(serializers.Serializer):
    sku = serializers.CharField(required=True, max_length=100)
    action = serializers.ChoiceField(
        choices=[
            (action.value, action.value) for action in AvailableStockManagerActions
        ]
    )


class StockItemSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if not obj.thumbnail or not obj.thumbnail.url:
            found_product = Product.objects.filter(
                stock_item=obj, thumbnail__isnull=False
            ).first()
            if found_product:
                return found_product.thumbnail.url

        return obj.thumbnail.url

    class Meta:
        model = StockItem
        fields = ["title", "thumbnail", "qr_code", "sku", "label"]
