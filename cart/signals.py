from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_order_total_on_order_item_save(sender, instance, created, **kwargs):
    """
    Update the order total when an order item is saved
    """
    print("Signal received")
    instance.order.recalculate_order()
