import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def update_product_status_on_stock_item_update(stock_item_id):
    """
    Update product status when stock item is updated
    """
    from shop.models import Product
    from stock.models import StockItem

    stock_item = StockItem.objects.get(id=stock_item_id)
    if stock_item.stock == 0:
        Product.objects.filter(
            stock_item=stock_item, status=Product.ProductStatus.PUBLISHED
        ).update(status=Product.ProductStatus.OUT_OF_STOCK)
    else:
        Product.objects.filter(
            stock_item=stock_item, status=Product.ProductStatus.OUT_OF_STOCK
        ).update(status=Product.ProductStatus.PUBLISHED)
    logger.info(f"Updated product status for stock item {stock_item_id}")
