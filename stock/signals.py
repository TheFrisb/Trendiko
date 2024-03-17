from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import Product
from stock.models import ReservedStockItem, StockItem


@receiver(post_save, sender=ReservedStockItem)
def update_order_total_on_order_item_save(sender, instance, created, **kwargs):
    """
    If quantity of reserved stock is depleted to 0, remove the reserved stock item
    """
    if instance.quantity == 0 and not created:
        instance.delete()


@receiver(post_save, sender=StockItem)
def archive_products_if_stock_item_is_out_of_stock(sender, instance, created, **kwargs):
    """
    If stock item is out of stock, archive the product
    """
    if instance.stock == 0:
        Product.objects.filter(stock_item=instance).update(
            status=Product.ProductStatus.ARCHIVED
        )
