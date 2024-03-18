from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cart.models import Order
from stock.models import ReservedStockItem


@receiver(pre_save, sender=Order)
@transaction.atomic
def change_reserved_items_status_on_order_status_change(sender, instance, **kwargs):
    """
    If the order is created, and its status is changed to "DELETED" from PENDING OR CONFIRMED, or changed to PENDING OR CONFIRMED
    from DELETED, fetch the orderItems and their reserved stocks, and change their statuses accordingly
    """

    if instance.pk is None:
        return

    apply_status = None

    if instance.status == Order.OrderStatus.DELETED:
        apply_status = ReservedStockItem.Status.ARCHIVED
    elif instance.status in [Order.OrderStatus.PENDING, Order.OrderStatus.CONFIRMED]:
        apply_status = ReservedStockItem.Status.PENDING

    for order_item in instance.order_items.all():
        for item in order_item.reserved_stock_items.all():
            if apply_status == ReservedStockItem.Status.PENDING:
                if item.quantity > 0:
                    item.status = apply_status
                    item.save()
            else:
                item.status = apply_status
                item.save()
