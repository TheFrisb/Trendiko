from rest_framework.exceptions import NotFound

from cart.models import CartItem, Cart
from common.exceptions import OutOfStockException
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
