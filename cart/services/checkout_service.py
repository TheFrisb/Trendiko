import uuid

from django.db import transaction
from rest_framework.exceptions import ValidationError

from cart.models import ShippingDetails, OrderItem, Order
from common.exceptions import OutOfStockException
from common.mailer.MailJetClient import MailJetClient
from shop.models import Product
from stock.models import ImportItem, ReservedStockItem


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

        if shipping_details.email:
            result = self.email_client.send_mail(
                "Потврда за нарачка",
                f"Вашата нарачка е успешно примена. Вашата нарачка е под број {order.tracking_number}.",
                shipping_details.email,
            )

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
            tracking_number=self.generate_tracking_number(),
            ip=self.get_ip_addr(),
            user_agent=self.get_user_agent(),
        )
        order.generate_barcode()

        return order

    def generate_tracking_number(self):
        """
        Generate a tracking number for an order.
        :return: str: The generated tracking number.
        """
        return str(uuid.uuid4())

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
        )

        try:
            reserved_stock_items = self.reserve_stock_for_order_item(order_item)
            order_item.reserved_stock_items.set(reserved_stock_items)
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
            )

        try:
            reserved_stock_items = self.reserve_stock_for_order_item(order_item)
            order_item.reserved_stock_items.set(reserved_stock_items)
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
        if order_item_id != check_promotion["order_item"].id:
            raise ValidationError(
                {"message": "The order item with the specified ID does not exist."}
            )

        if promotion_price != check_promotion["promotion_price"]:
            raise ValidationError({"message": "The promotion price is invalid."})

        return check_promotion["order_item"]

    @transaction.atomic
    def reserve_stock_for_order_item(self, order_item):
        """
        Reserve stock for an order item.

        Args:
            order_item (OrderItem): The order item for which stock should be reserved.
        """
        quantity_to_be_reserved = order_item.quantity
        import_items = ImportItem.objects.filter(
            stock_item=order_item.stock_item, quantity__gt=0
        ).order_by("created_at")
        reserved_stock_items = []

        for import_item in import_items:
            if quantity_to_be_reserved == 0:
                break
            if (
                import_item.calculate_max_available_reservation()
                >= quantity_to_be_reserved
            ):
                reserved_stock_item = ReservedStockItem.objects.create(
                    order_item=order_item,
                    import_item=import_item,
                    initial_quantity=quantity_to_be_reserved,
                )
                quantity_to_be_reserved = 0
            else:
                removeable_quantity = import_item.calculate_max_available_reservation()
                reserved_stock_item = ReservedStockItem.objects.create(
                    order_item=order_item,
                    import_item=import_item,
                    initial_quantity=removeable_quantity,
                )
                quantity_to_be_reserved -= removeable_quantity

            reserved_stock_items.append(reserved_stock_item)
        if quantity_to_be_reserved > 0:
            available_quantity = order_item.quantity - quantity_to_be_reserved
            raise OutOfStockException(order_item.quantity, available_quantity)

        return reserved_stock_items

    def get_ip_addr(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", None)
        return ip

    def get_user_agent(self):
        return self.request.META.get("HTTP_USER_AGENT", None)
