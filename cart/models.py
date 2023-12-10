from django.db import models
from shop.models import Product, ProductAttribute
from common.models import TimeStampedModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Cart(TimeStampedModel):
    """
    The Cart model represents a shopping cart.
    It contains a foreign key to the user who owns the cart and a session key.
    It also includes methods to calculate the total price and total quantity of items in the cart.

    The user field is nullable because the cart can be owned by a user or by a session.

    The only logged-in users in this website will be the admins and the staff,
    so this field is set here only for future use should they choose to add a user account system.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    session_key = models.CharField(
        max_length=40, null=True, blank=True, default=None, db_index=True
    )

    @property
    def get_total(self):
        """
        Calculate the total price of all items in the cart.

        Returns:
            int: The total price of all items in the cart.
        """

        return sum(item.total_price for item in self.cart_items.all())

    @property
    def get_total_quantity(self):
        """
        Calculate the total quantity of all items in the cart.

        Returns:
            int: The total quantity of all items in the cart.
        """

        return sum(item.quantity for item in self.cart_items.all())

    def __str__(self):
        return f"Cart id: {self.id}, Total: {self.get_total}, Total Quantity: {self.get_total_quantity}"


class CartItem(TimeStampedModel):
    """
    The CartItem model represents an item in a shopping cart.
    It contains foreign keys to the cart and product associated with the item.
    It also includes a method to calculate the total price of the item.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    type = models.CharField(
        max_length=20,
        choices=Product.ProductType.choices,
        default=Product.ProductType.SIMPLE,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, null=True, blank=True
    )

    @property
    def total_price(self):
        """
        Calculate the total price of the cart item.

        Returns:
            int: The total price of the cart item.
        """

        if self.attribute:
            return self.attribute.price * self.quantity

        return self.product.selling_price * self.quantity

    @property
    def price(self):
        """
        Get the price of the cart item.

        Returns:
             int: The price of the cart item.
        """
        if self.attribute:
            return self.attribute.price

        return self.product.selling_price

    def __str__(self):
        return self.product.title


class Order(TimeStampedModel):
    """
    The Order model represents an order. It contains a foreign key to the user who placed the order and a session key.
    It also includes fields for the order status, whether the order has free shipping,
    and the subtotal, total, and shipping prices.
    """

    class OrderStatus(models.TextChoices):
        """Order Status"""

        PROCESSING = "processing", _("Processing")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    session_key = models.CharField(max_length=40, null=True, blank=True, default=None)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING
    )
    has_free_shipping = models.BooleanField(default=False)
    subtotal_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    shipping_price = models.IntegerField(default=130)


class OrderItem(TimeStampedModel):
    """
    The OrderItem model represents an item in an order.
    It contains foreign keys to the order and product associated with the item.
    It also includes a method to calculate the total price of the item.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    type = models.CharField(
        max_length=20,
        choices=Product.ProductType.choices,
        default=Product.ProductType.SIMPLE,
    )
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, null=True, blank=True
    )

    @property
    def total_price(self):
        """
        Calculate the total price of the order item.

        Returns:
            int: The total price of the order item.
        """
        return self.price * self.quantity


class ShippingDetails(TimeStampedModel):
    """
    The ShippingDetails model represents the shipping details for an order.
    It contains a foreign key to the associated order.
    It also includes fields for the first name, last name, address, city,
    and phone number for shipping.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="shipping_details"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
