from rest_framework import serializers
from rest_framework.exceptions import NotFound

from stock.models import StockItem
from stock.serializers import AvailableStockManagerActions


class StockItemService:
    def manage_stock_item_by_action(self, serializer):
        action = serializer.validated_data["action"]
        sku = serializer.validated_data["sku"]

        try:
            stock_item = StockItem.objects.get(sku=sku)

        except StockItem.DoesNotExist:
            raise NotFound({"sku": "StockItem not found " + str(sku)})

        if action == AvailableStockManagerActions.ADD_QUANTITY.value:
            return self.add_stock(stock_item)

        elif action == AvailableStockManagerActions.REMOVE_QUANTITY.value:
            return self.remove_stock(stock_item)

        else:
            raise serializers.ValidationError(
                {"action": "Action not allowed " + str(action)}
            )

    def add_stock(self, stock_item):
        # stock_item.quantity += 1
        stock_item.save()

        return stock_item

    def remove_stock(self, stock_item):
        # stock_item.quantity -= 1
        stock_item.save()

        return stock_item
