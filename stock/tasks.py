import logging

from celery import shared_task
from django.db import transaction
from django.db.models import Sum

logger = logging.getLogger(__name__)


@shared_task
def update_product_status_on_stock_item_update(stock_item_id):
    from shop.models import Product, ProductAttribute
    from stock.models import StockItem

    stock_item = StockItem.objects.get(id=stock_item_id)

    with transaction.atomic():
        # Fetching products and attributes together if possible
        products = Product.objects.filter(stock_item=stock_item)
        if products.exists():
            # Bulk update preparation
            updated_products = []
            for product in products:
                new_status = (
                    Product.ProductStatus.PUBLISHED
                    if stock_item.stock > 0
                    else Product.ProductStatus.OUT_OF_STOCK
                )
                if product.status != new_status:
                    product.status = new_status
                    updated_products.append(product)

            Product.objects.bulk_update(updated_products, ["status"])
        else:
            attributes = (
                ProductAttribute.objects.filter(stock_item=stock_item)
                .select_related("product")
                .distinct("product")
            )
            for attribute in attributes:
                product = attribute.product
                product_stock = (
                    ProductAttribute.objects.filter(product=product).aggregate(
                        total_stock=Sum("stock_item__stock")
                    )["total_stock"]
                    or 0
                )
                new_status = (
                    Product.ProductStatus.PUBLISHED
                    if product_stock > 0
                    else Product.ProductStatus.OUT_OF_STOCK
                )
                if product.status != new_status:
                    product.status = new_status
                    product.save()
        logger.info(f"Updated product status for stock item {stock_item_id}")
