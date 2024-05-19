from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from stock.models import StockItem, ReservedStockItem
from stock.tasks import update_product_status_on_stock_item_update


@receiver(post_save, sender=StockItem)
def archive_products_if_stock_item_is_out_of_stock(sender, instance, created, **kwargs):
    """
    If stock item is out of stock, archive the product
    """
    if instance.pk is not None:
        update_product_status_on_stock_item_update.delay(instance.id)


@receiver(pre_delete, sender=ReservedStockItem)
def update_stock_on_reserved_stock_item_delete(sender, instance, **kwargs):
    """
    When a reserved stock item is deleted, update the stock item's reserved stock
    """
    if instance.status == ReservedStockItem.Status.PENDING:
        import_item = instance.import_item
        import_item.quantity += instance.quantity
        import_item.save()


# detest reserved stock item status change
@receiver(pre_save, sender=ReservedStockItem)
def update_stock_on_reserved_stock_item_status_change(sender, instance, **kwargs):
    """
    When a reserved stock item status is changed, update the stock item's reserved stock
    """
    # if the status is changed from pending to archived
    if instance.pk is not None:
        old_instance = ReservedStockItem.objects.get(pk=instance.pk)
        if (
            old_instance.status == ReservedStockItem.Status.PENDING
            and instance.status == ReservedStockItem.Status.ARCHIVED
        ):
            import_item = instance.import_item
            import_item.quantity += instance.quantity
            import_item.save()
        if (
            old_instance.status == ReservedStockItem.Status.ARCHIVED
            and instance.status == ReservedStockItem.Status.PENDING
        ):
            import_item = instance.import_item
            import_item.quantity -= instance.quantity
            import_item.save()
