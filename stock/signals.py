from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from stock.models import StockItem, ReservedStockItem
from stock.tasks import update_product_status_on_stock_item_update


@receiver(post_save, sender=StockItem)
def archive_products_if_stock_item_is_out_of_stock(sender, instance, created, **kwargs):
    """
    If stock item is out of stock, archive the product
    """
    if not created:
        update_product_status_on_stock_item_update.delay(instance.id)


@receiver(pre_delete, sender=ReservedStockItem)
def update_stock_on_reserved_stock_item_delete(sender, instance, **kwargs):
    """
    When a reserved stock item is deleted, update the stock item's reserved stock
    """
    if instance.status == ReservedStockItem.Status.PENDING:
        import_item = instance.import_item
        import_item.reserved_stock -= instance.quantity
        import_item.save()
