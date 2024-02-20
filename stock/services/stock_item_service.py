from rest_framework import serializers
from rest_framework.exceptions import NotFound

from stock.models import StockItem, ImportItem
from stock.serializers import AvailableStockManagerActions


class StockItemService:
    def manage_stock_item_by_action(self, serializer):
        action = serializer.validated_data["action"]
        sku = serializer.validated_data["sku"]

        try:
            stock_item = StockItem.objects.get(sku=sku)

        except StockItem.DoesNotExist:
            raise NotFound({"sku": "StockItem not found " + str(sku)})

        import_item = (
            ImportItem.objects.filter(stock_item=stock_item, quantity__gt=0)
            .order_by("created_at")
            .first()
        )

        if action == AvailableStockManagerActions.ADD_QUANTITY.value:
            if import_item:
                import_item.quantity += 1
                import_item.save()
            return self.add_stock(stock_item)

        elif action == AvailableStockManagerActions.REMOVE_QUANTITY.value:
            if import_item:
                import_item.quantity -= 1
                import_item.save()
            return self.remove_stock(stock_item)

        else:
            raise serializers.ValidationError(
                {"action": "Action not allowed " + str(action)}
            )

    def add_stock(self, stock_item):
        stock_item.stock += 1
        stock_item.save()

        return stock_item

    def remove_stock(self, stock_item):
        stock_item.stock -= 1
        stock_item.save()

        return stock_item
