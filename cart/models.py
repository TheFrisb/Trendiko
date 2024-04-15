import base64
from datetime import datetime
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML

from common.models import TimeStampedModel, LoggableModel
from shop.models import Product, ProductAttribute


# Create your models here.


def invoice_upload_to(instance, filename):
    today = datetime.now()
    return f"{today.year}/{today.month}/{today.day}/{filename}"


class Cart(TimeStampedModel):
    """
    The Cart model represents a shopping cart.
    It contains a foreign key to the user who owns the cart and a session key.
    It also includes methods to calculate the total sale_price and total quantity of items in the cart.

    The user field is nullable because the cart can be owned by a user or by a session.

    The only logged-in users in this website will be the admins and the staff,
    so this field is set here only for future use should they choose to add a user account system.
    """

    class CartStatus(models.TextChoices):
        """Cart Status"""

        ACTIVE = "active", _("Активна")
        ABANDONED = "abandoned", _("Напуштена")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
        db_index=True,
    )
    session_key = models.CharField(max_length=40, default=None, db_index=True)

    @property
    def has_free_shipping(self):
        """
        Check if the cart has free shipping.

        Returns:
            bool: True if the cart has free shipping, False otherwise.
        """
        product_has_free_shipping = any(
            item.product.has_free_shipping for item in self.cart_items.all()
        )
        cart_has_free_shipping = self.get_items_total >= 1500
        return product_has_free_shipping or cart_has_free_shipping

    @property
    def get_items_total(self):
        """
        Calculate the total sale_price of all items in the cart.

        Returns:
            int: The total sale_price of all items in the cart.
        """
        return sum(item.total_price for item in self.cart_items.all())

    @property
    def get_total_price(self):
        """
        Calculate the total price of all items in the cart including shipping and handling/provision fee.
        :return:
        """
        has_free_shipping = self.has_free_shipping
        items_total = self.get_items_total + 20

        if has_free_shipping:
            return items_total

        return items_total + 130

    @property
    def get_total_quantity(self):
        """
        Calculate the total quantity of all items in the cart.

        Returns:
            int: The total quantity of all items in the cart.
        """

        return sum(item.quantity for item in self.cart_items.all())

    def is_empty(self):
        """
        Check if the cart is empty.

        Returns:
            bool: True if the cart is empty, False otherwise.
        """
        return self.cart_items.count() == 0

    def __str__(self):
        return f"Cart id: {self.id}, Total: {self.get_items_total}, Total Quantity: {self.get_total_quantity}"


class CartItem(TimeStampedModel):
    """
    The CartItem model represents an item in a shopping cart.
    It contains foreign keys to the cart and product associated with the item.
    It also includes a method to calculate the total sale_price of the item.
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
    def sale_price(self):
        """
        Get the sale_price of the cart item.

        Returns:
            int: The sale_price of the cart item.
        """
        if self.attribute:
            return self.attribute.sale_price

        return self.product.selling_price

    @property
    def title(self):
        """
        Get the title of the cart item.

        Returns:
            str: The title of the cart item.
        """
        if self.attribute:
            return f"{self.product.title} - {self.attribute.title}"
        return self.product.title

    @property
    def thumbnails(self):
        """
        Get the thumbnails of the cart item.

        Returns:
            str: The thumbnails of the cart item.
        """
        if self.product.type == Product.ProductType.VARIABLE:
            return self.attribute.get_thumbnail_loops()
        return {
            "webp": self.product.thumbnail_loop.url,
            "jpg": self.product.thumbnail_loop_as_jpeg.url,
        }

    @property
    def total_price(self):
        """
        Calculate the total sale_price of the cart item.

        Returns:
            int: The total sale_price of the cart item.
        """

        if self.attribute:
            return self.attribute.sale_price * self.quantity

        return self.product.selling_price * self.quantity

    def get_stock_item(self):
        """
        Get the stock item of the cart item.

        Returns:
            StockItem: The stock item of the cart item.
        """
        if self.attribute:
            return self.attribute.stock_item
        return self.product.stock_item

    def __str__(self):
        return self.product.title


class Order(TimeStampedModel, LoggableModel):
    """
    The Order model represents an order. It contains a foreign key to the user who placed the order and a session key.
    It also includes fields for the order status, whether the order has free shipping,
    and the subtotal, total, and shipping prices.
    """

    class OrderStatus(models.TextChoices):
        """Order Status"""

        PENDING = "pending", _("непотврдени")
        CONFIRMED = "confirmed", _("потврдени")
        DELETED = "deleted", _("избришени")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    session_key = models.CharField(max_length=40)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )
    shipping_price = models.IntegerField(default=130)
    subtotal_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    tracking_number = models.CharField(max_length=100, unique=True, db_index=True)
    has_free_shipping = models.BooleanField(default=False)
    mail_is_sent = models.BooleanField(default=False)
    exportable_date = models.DateTimeField(default=now)

    def get_absolute_url(self):
        """
        Get the absolute url of the order.

        Returns:
            str: The absolute url of the order.
        """
        return reverse(
            "shop:thank_you_page", kwargs={"tracking_number": self.tracking_number}
        )

    @property
    def get_shipping_method(self):
        """
        Get the shipping method of the order.

        Returns:
            str: The shipping method of the order.
        """
        if self.has_free_shipping:
            return "Бесплатна достава"
        return "130 ден"

    def make_thank_you_product(self):
        # check if order is not older than 5 minutes
        if (timezone.now() - self.created_at).seconds > 180:
            return None

        if self.order_items.filter(
            promotion_type=OrderItem.PromotionType.THANK_YOU
        ).exists():
            return None

        order_item = self.order_items.order_by("created_at").first()
        price = int(order_item.price * 0.9)
        # make time_left as xx:xx
        minutes_left = 2 - (timezone.now() - self.created_at).seconds // 60
        seconds_left = 59 - (timezone.now() - self.created_at).seconds % 60

        return {
            "promotion_price": price,
            "order_item": order_item,
            "readable_name": order_item.get_readable_name,
            "time_left": f"{minutes_left:02d}:{seconds_left:02d}",
        }

    def get_shipping_price(self):
        """
        Get the shipping price of the order.

        Returns:
            int: The shipping price of the order.
        """
        if self.has_free_shipping:
            return 0
        return 130

    def recalculate_order(self):
        """
        Recalculate the prices of the order.
        """
        self.subtotal_price = sum(item.total_price for item in self.order_items.all())
        if self.subtotal_price >= 1500 or any(
            item.product.has_free_shipping for item in self.order_items.all()
        ):
            self.has_free_shipping = True

        if self.has_free_shipping:
            self.total_price = self.subtotal_price + 20
        else:
            self.total_price = self.subtotal_price + 130

        self.save()

    # def generate_invoice(self):
    #     """
    #     Generate an invoice for the order.
    #     """
    #     if self.invoice.name:
    #         self.invoice.delete()
    #
    #     context = {
    #         "order": self,
    #         "order_items": self.order_items.all(),
    #         "shipping_details": self.shipping_details,
    #     }
    #
    #     html_string = render_to_string("shop_manager/pdf_template.html", context)
    #
    #     pdf_bytes = HTML(
    #         string=html_string, base_url=settings.WEBSITE_BASE_URL
    #     ).write_pdf()
    #
    #     pdf_file = BytesIO(pdf_bytes)
    #     pdf_file.name = f"order_{self.id}_invoice.pdf"
    #
    #     self.invoice.save(pdf_file.name, pdf_file)

    def generate_invoice_pdf(self, base_url, write_to=None, show_details=True):
        context = {
            "order": self,
            "order_items": self.order_items.all(),
            "shipping_details": self.shipping_details,
            "show_details": show_details,
        }

        html_string = render_to_string("shop_manager/pdf_template.html", context)

        if write_to:
            HTML(string=html_string, base_url=base_url).write_pdf(target=write_to)
            return write_to

        return HTML(string=html_string, base_url=base_url).write_pdf()

    def generate_barcode(self):
        barcode_content = self.make_barcode_content()
        code128 = barcode.get_barcode_class("code128")
        barcode_image = code128(barcode_content, writer=ImageWriter())

        buffer = BytesIO()
        barcode_image.write(buffer)
        buffer.seek(0)

        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{base64_image}"

    def get_invoice_number(self):
        """
        Get the invoice number of the order.

        Returns:
            str: The invoice number of the order.
        """
        year = str(self.created_at.year)[-2:]
        return f"{self.id}/{year}"

    @property
    def get_total_quantity(self):
        """
        Calculate the total quantity of all items in the order.

        Returns:
            int: The total quantity of all items in the order.
        """
        return sum(item.quantity for item in self.order_items.all())

    def make_barcode_content(self):
        id_str = str(self.id).zfill(5)
        return f"TR{id_str}"

    def __str__(self):
        return f"Order id: {self.id}, Status: {self.status}, Total: {self.total_price}, Created at: {self.created_at}"


class OrderItem(TimeStampedModel):
    """
    The OrderItem model represents an item in an order.
    It contains foreign keys to the order and product associated with the item.
    It also includes a method to calculate the total sale_price of the item.
    """

    class PromotionType(models.TextChoices):
        """Order Status"""

        THANK_YOU = "thank_you", _("thank_you")
        SIDECART = "sidecart", _("sidecart")

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="order_items", null=True
    )
    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
    )
    reserved_stock_items = models.ManyToManyField(
        "stock.ReservedStockItem", related_name="order_items"
    )
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    type = models.CharField(
        max_length=20,
        choices=Product.ProductType.choices,
        default=Product.ProductType.SIMPLE,
    )
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.SET_NULL, null=True, blank=True
    )
    promotion_type = models.CharField(
        max_length=25, choices=PromotionType, default=None, null=True, blank=True
    )

    @property
    def get_thumbnail_loops(self):
        """
        Get the thumbnails of the order item.

        Returns:
            str: The thumbnails of the order item.
        """
        if self.attribute:
            return self.attribute.get_thumbnail_loops()
        return {
            "webp": self.product.thumbnail_loop.url,
            "jpg": self.product.thumbnail_loop_as_jpeg.url,
        }

    @property
    def get_thumbnails(self):
        """
        Get the thumbnails of the order item.

        Returns:
            str: The thumbnails of the order item.
        """
        if self.attribute:
            return self.attribute.get_thumbnails()
        return {
            "webp": self.product.thumbnail.url,
            "jpg": self.product.thumbnail_as_jpeg.url,
        }

    @property
    def total_price(self):
        """
        Calculate the total sale_price of the order item.

        Returns:
            int: The total sale_price of the order item.
        """
        return self.price * self.quantity

    @property
    def get_readable_name(self):
        """
        Get the readable name of the order item.
        :return: str: The readable name of the order item.
        """
        if self.attribute:
            return f"{self.product.title} - {self.attribute.title}"

        return self.product.title


class ShippingDetails(TimeStampedModel):
    """
    The ShippingDetails model represents the shipping details for an order.
    It contains a foreign key to the associated order.
    It also includes fields for the first name, last name, address, city,
    and phone number for shipping.
    """

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="shipping_details"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20)
    comment = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    @property
    def full_name(self):
        """
        Get the full name of the customer.
        :return: str: The full name of the customer.
        """
        return f"{self.first_name} {self.last_name}"


class AbandonedCartDetails(TimeStampedModel):
    """
    The AbandonedCartDetails model represents the details of an abandoned cart.
    It contains a foreign key to the associated cart.
    It also includes fields for the first name, last name, address, city,
    and phone number for shipping.
    """

    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, related_name="abandoned_cart_details"
    )
    full_name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
