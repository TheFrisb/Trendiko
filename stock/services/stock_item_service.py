from rest_framework import serializers
from rest_framework.exceptions import NotFound

from common.exceptions import OutOfStockException
from stock.models import StockItem, ImportItem, ReservedStockItem
from stock.serializers import AvailableStockManagerActions


class StockItemService:
    def manage_stock_item_by_action(self, serializer):
        action = serializer.validated_data["action"]
        sku = serializer.validated_data["sku"]

        try:
            stock_item = StockItem.objects.get(sku=sku)
        except StockItem.DoesNotExist:
            raise NotFound("Stock item not found")

        import_items = ImportItem.objects.filter(stock_item=stock_item).order_by(
            "created_at"
        )

        if action == AvailableStockManagerActions.ADD_QUANTITY.value:
            import_item = import_items.last()
            import_item.quantity += 1
            import_item.save()
            return stock_item

        elif action == AvailableStockManagerActions.REMOVE_QUANTITY.value:
            reserved_stock_item = (
                ReservedStockItem.objects.filter(
                    order_item__stock_item=stock_item,
                    quantity__gt=0,
                    status=ReservedStockItem.Status.PENDING,
                )
                .prefetch_related("import_item")
                .order_by("import_item__created_at")
                .first()
            )
            if reserved_stock_item:
                reserved_stock_item.quantity -= 1
                reserved_stock_item.save()

                import_item = reserved_stock_item.import_item
                import_item.quantity -= 1
                import_item.save()
                return stock_item
            else:
                message = "No reserved stock found for this product"
                raise OutOfStockException(1, 0, {"message": message})

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
