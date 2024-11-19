from rest_framework.exceptions import NotFound

from cart.models import CartItem, Cart, AbandonedCartDetails
from common.exceptions import OutOfStockException
from shop.models import CartOffers
from shop.services.product_service import ProductService
from stock.services.stock_validator import StockValidator


class CartService:
    """
    Service class for handling cart-related operations.

    Attributes:
        cart (Cart): The cart instance that this service will operate on.
        product_service (ProductService): The product service instance that this service will use.
    """

    def __init__(self, cart, product_service):
        """
        Initialize the CartService with a cart instance.
        Inject the ProductService instance that this service will use.

        Args:
            cart (Cart): The cart instance that this service will operate on.
        """
        self.cart = cart
        self.product_service = product_service
        self.stock_validator = StockValidator()

    def add_product_to_cart(self, data):
        """
        Add a product to the cart or update its quantity if it's already in the cart.

        This method uses the ProductService to validate the incoming data and get the product,
        product type, attribute (if any), and quantity.
        It then adds the product to the cart or updates its quantity if it's already in the cart.

        Args:
            data (dict): The incoming serialized data to be validated and added to the cart.
             It should include 'product_id', 'product_type', 'quantity', and optionally 'attribute_id'.

        Returns:
            CartItem: The cart item instance that was created or updated.

        Raises:
            NotFound: If the cart item does not exist for this cart.
            ValidationError: If the product does not exist, is not published,
             or its type does not match the provided type.
            ValidationError: If the product is variable and no attribute ID is provided,
             or the provided attribute ID does not correspond to an existing attribute of the product.
        """
        (
            product,
            product_type,
            attribute,
            quantity,
        ) = self.product_service.validate_product(data)

        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            type=product_type,
            attribute=attribute,
            cart_offer=None,
            defaults={"quantity": quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def remove_from_cart(self, pk):
        """
        Remove a product from the cart.

        Args:
            pk (int): The primary key of the cart item to be removed.
        """
        cart_item = self.fetch_cart_item_or_throw(pk)
        cart_item.delete()

    def update_cart_item(self, pk, quantity):
        """
        Update the quantity of a product in the cart.

        Args:
            pk (int): The primary key of the cart item to be updated.
            quantity (int): The new quantity of the product.

        Returns:
            CartItem: The cart item instance that was updated.
        """
        cart_item = self.fetch_cart_item_or_throw(pk)
        if (
            not self.stock_validator.check_stock_item_stock(
                cart_item.get_stock_item(), quantity
            )
            and quantity > cart_item.quantity
        ):
            message = f"Немаме доволно парчиња на залиха од овој производ."

            extraDict = {
                "cart_item_id": cart_item.id,
                "message": message,
            }

            raise OutOfStockException(
                quantity, cart_item.get_stock_item().stock, extraDict
            )
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def fetch_cart_item_or_throw(self, pk):
        """
        Fetch a cart item from the cart.

        Args:
            pk (int): The primary key of the cart item to be fetched.

        Returns:
            CartItem: The cart item instance that was fetched.

        Raises:
            NotFound: If the cart item does not exist for this cart.
        """
        try:
            cart_item = self.cart.cart_items.get(pk=pk)
        except CartItem.DoesNotExist:
            raise NotFound(
                {"cart_item": f"Cart item with id {pk} does not exist for this cart"}
            )
        return cart_item

    def save_abandoned_cart_details(self, data):
        """
        Save the details of an abandoned cart.

        Args:
            data (dict): The details of the abandoned cart.

        Returns:
            Cart: The cart instance that was updated with the abandoned cart details.
        """
        abandoned_details = AbandonedCartDetails.objects.filter(cart=self.cart).first()

        if not abandoned_details:
            abandoned_details = AbandonedCartDetails.objects.create(
                cart=self.cart, **data
            )

        else:
            if data.get("email") != "":
                abandoned_details.email = data.get("email")
            if data.get("phone") != "":
                abandoned_details.phone = data.get("phone")
            if data.get("full_name") != "":
                abandoned_details.full_name = data.get("full_name")
            if data.get("address") != "":
                abandoned_details.address = data.get("address")
            if data.get("city") != "":
                abandoned_details.city = data.get("city")

            abandoned_details.save()

        return abandoned_details

    def add_cart_offer_to_cart(self, data):
        cart_offer = CartOffers.objects.get(pk=data["cart_offer_id"])

        validation_data = {
            "product_id": cart_offer.product.id,
            "product_type": cart_offer.product.type,
            "quantity": 1,
            "attribute_id": None,
        }

        (
            product,
            product_type,
            attribute,
            quantity,
        ) = self.product_service.validate_product(validation_data)

        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=cart_offer.product,
            type=product_type,
            attribute=attribute,
            cart_offer=cart_offer,
            quantity=1,
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item
