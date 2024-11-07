from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from cart.models import ShippingDetails, OrderItem, Order
from cart.tasks import generate_invoice_and_send_email_to_order
from common.exceptions import OutOfStockException
from common.mailer.MailJetClient import MailJetClient
from common.utils import get_ip_addr, get_user_agent
from shop.models import Product


class CheckoutService:
    """
    Service class for handling the checkout process in an e-commerce application.

    Attributes:
        cart (Cart): The cart instance that this service will operate on.
    """

    def __init__(self, request):
        """
        Initialize the CheckoutService with a cart instance.

        Args:
            cart (Cart): The cart instance that this service will operate on.
        """
        self.request = request
        self.cart = request.cart
        self.email_client = MailJetClient()

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

        generate_invoice_and_send_email_to_order.apply_async(
            (order.id,), countdown=360
        )  # 360 seconds = 6 minutes

        return order

    @transaction.atomic
    def add_order_item_to_existing_order(self, data):
        """
        Add an order item to an existing order.

        Args:
            data (dict): A dictionary containing the order item ID and quantity.

        Returns:
            Order: The order instance that was updated.
        """
        order_id = data["order_id"]
        order_item_id = data["order_item_id"]
        quantity = data["quantity"]
        tracking_number = data["tracking_code"]
        promotion_price = data["promotion_price"]

        try:
            # get order with its orderItems
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError(
                {"message": "The order with the specified ID does not exist."}
            )

        if order.tracking_number != tracking_number:
            raise ValidationError({"message": "The tracking number is invalid."})

        if (timezone.now() - order.created_at).seconds > 300:
            raise ValidationError(
                {"message": "The promotion for this order has expired."}
            )

        copy_order_item = self.validate_thank_you_order_item(
            order, order_item_id, promotion_price
        )

        return self.add_thank_you_order_item_to_order(
            copy_order_item, order, quantity, promotion_price
        )

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
            ip=get_ip_addr(self.request),
            user_agent=get_user_agent(self.request),
        )

        return order

    @transaction.atomic
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
            stock_item=self.get_stock_item_by_cart_item_type(cart_item),
            attribute=cart_item.attribute,
            is_cart_offer=cart_item.is_cart_offer,
        )

        try:
            order_item.reserve_stock_for_order_item()
        except OutOfStockException as e:
            available_quantity = e.available_quantity
            requested_quantity = e.requested_quantity

            if available_quantity <= 0:
                message = f'Производот "{cart_item.title}" е распродаден.'
            else:
                message = f'Имаме само {available_quantity} на залиха од продуктот "{cart_item.title}"'

            extra_dict = {
                "message": message,
                "cart_item_id": cart_item.id,
            }
            # re raise the exception with the message
            raise OutOfStockException(
                requested_quantity, available_quantity, extra_dict
            )

        return order_item

    @transaction.atomic
    def add_thank_you_order_item_to_order(
        self, copy_order_item, order, quantity, price
    ):
        order_item = order.order_items.filter(
            product=copy_order_item.product,
            promotion_type=OrderItem.PromotionType.THANK_YOU,
            price=price,
        ).first()

        if order_item:
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                order=order,
                product=copy_order_item.product,
                quantity=quantity,
                price=price,
                type=copy_order_item.type,
                attribute=copy_order_item.attribute,
                stock_item=copy_order_item.stock_item,
                promotion_type=OrderItem.PromotionType.THANK_YOU,
                rabat=10,
            )

        try:
            order_item.reserve_stock_for_order_item()
        except OutOfStockException as e:
            available_quantity = e.available_quantity
            requested_quantity = e.requested_quantity

            if available_quantity <= 0:
                message = (
                    f'Производот "{copy_order_item.get_readable_name}" е распродаден.'
                )
            else:
                message = f'Имаме само {available_quantity} од "{copy_order_item.get_readable_name}" на залиха.'

            extra_dict = {
                "message": message,
            }
            # re raise the exception with the message
            raise OutOfStockException(
                requested_quantity, available_quantity, extra_dict
            )
        order_item.order.recalculate_order()
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
            municipality=shipping_details["municipality"],
            email=shipping_details["email"],
        )

        return shipping_details

    def get_stock_item_by_cart_item_type(self, cart_item):
        """
        Calculate the stock item for a given cart item.

        Args:
            cart_item (CartItem): The cart item to be added to the order.

        Returns:
            StockItem: The stock item instance that was created.
        """
        if cart_item.type == Product.ProductType.VARIABLE:
            return cart_item.attribute.stock_item

        return cart_item.product.stock_item

    def validate_thank_you_order_item(self, order, order_item_id, promotion_price):
        check_promotion = order.make_thank_you_product()
        if not check_promotion:
            raise ValidationError(
                {
                    "message": "The order promotion is expired."
                    "Please contact the administrator."
                }
            )

        if order_item_id != check_promotion["order_item"].id:
            raise ValidationError(
                {"message": "The order item with the specified ID does not exist."}
            )

        if promotion_price != check_promotion["promotion_price"]:
            raise ValidationError({"message": "The promotion price is invalid."})

        return check_promotion["order_item"]
