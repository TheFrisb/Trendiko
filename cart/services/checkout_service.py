import uuid

from django.db import transaction
from rest_framework.exceptions import ValidationError

from cart.models import ShippingDetails, OrderItem, Order


class CheckoutService:
    """
    Service class for handling the checkout process in an e-commerce application.

    Attributes:
        cart (Cart): The cart instance that this service will operate on.
    """

    def __init__(self, cart):
        """
        Initialize the CheckoutService with a cart instance.

        Args:
            cart (Cart): The cart instance that this service will operate on.
        """
        self.cart = cart

    @transaction.atomic
    def checkout(self, shipping_details):
        """
        Initiate the checkout process. This method is responsible for creating an order,
        creating order items for each item in the cart, creating shipping details for the order,
        and clearing the cart.

        Args:
            shipping_details (dict): A dictionary containing the shipping details for the order.

        Returns:
            Order: The order instance that was created.
        """
        if self.cart.is_empty():
            raise ValidationError(
                {
                    "message": "The cart is empty. Add items to the cart before checking out."
                }
            )

        order = self.create_order()

        for cart_item in self.cart.cart_items.all():
            order_item = self.create_order_item(cart_item, order)

        shipping_details = self.create_shipping_details(shipping_details, order)

        self.cart.delete()

        return order

    def create_order(self):
        """
        Create an order instance.

        Returns:
            Order: The order instance that was created.
        """
        order = Order.objects.create(
            user=None,  # see cart/models.py
            session_key=self.cart.session_key,
            subtotal_price=self.cart.get_items_total,
            total_price=self.cart.get_total_price,
            has_free_shipping=self.cart.has_free_shipping,
            tracking_number=self.generate_tracking_number(),
        )

        return order

    def generate_tracking_number(self):
        """
        Generate a tracking number for an order.
        :return: str: The generated tracking number.
        """
        return str(uuid.uuid4())

    def create_order_item(self, cart_item, order):
        """
        Create an order item for a given cart item.

        Args:
            cart_item (CartItem): The cart item to be added to the order.
            order (Order): The order that the cart item belongs to.

        Returns:
            OrderItem: The order item instance that was created.
        """
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.sale_price,
            type=cart_item.type,
            attribute=cart_item.attribute,
        )

        return order_item

    def create_shipping_details(self, shipping_details, order):
        """
        Create shipping details for an order.

        Args:
            shipping_details (dict): A dictionary containing the shipping details for the order.
            order (Order): The order that the shipping details belong to.

        Returns:
            ShippingDetails: The shipping details instance that was created.
        """
        shipping_details = ShippingDetails.objects.create(
            order=order,
            first_name=shipping_details["first_name"],
            last_name=shipping_details["last_name"],
            address=shipping_details["address"],
            phone=shipping_details["phone"],
            city=shipping_details["city"],
        )

        return shipping_details
