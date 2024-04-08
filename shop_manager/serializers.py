from rest_framework import serializers

from cart.models import Order, Cart


class ChangeOrderStatusSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    new_status = serializers.ChoiceField(choices=Order.OrderStatus.choices)

    def validate(self, data):
        order_id = data.get("order_id")
        new_status = data.get("new_status")
        order = (
            Order.objects.filter(id=order_id)
            .prefetch_related("order_items", "order_items__reserved_stock_items")
            .first()
        )

        if not order:
            raise serializers.ValidationError("Order not found")

        if order.status == new_status:
            raise serializers.ValidationError("Order already has this status")

        data["order"] = order

        return data


class RemoveAbandonedCartSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(min_value=1)

    def validate(self, data):
        cart_id = data.get("cart_id")
        cart = Cart.objects.filter(id=cart_id, status=Cart.CartStatus.ABANDONED).first()

        if not cart:
            raise serializers.ValidationError("Cart not found")

        data["cart"] = cart

        return data
