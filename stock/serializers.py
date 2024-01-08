from enum import Enum

from rest_framework import serializers

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
    class Meta:
        model = StockItem
        fields = ["title", "thumbnail", "qr_code", "sku", "label"]
