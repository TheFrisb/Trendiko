from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from common.exceptions import OutOfStockException
from shop.models import Product, ProductAttribute
from stock.services.stock_validator import StockValidator


class ProductService:
    """
    Service class for handling product-related operations.
    """

    def __init__(self):
        """
        Initialize the ProductService.
        """
        self.stock_validator = StockValidator()

    def validate_product(self, data):
        """
        Validate the incoming data.

        This method checks if the product exists and is published, and if the product type matches the provided type.
        For variable products, it also checks if an attribute ID is provided and
        if it corresponds to an existing attribute of the product.

        Args:
            data (dict): The incoming data to be validated.
             It should include 'product_id', 'product_type', 'quantity', and optionally 'attribute_id'.

        Returns:
            tuple: A tuple containing the product instance, product type, attribute instance (if any), and quantity.

        Raises:
            NotFound: If the product does not exist or the attribute does not exist for the provided product.
            PermissionDenied: If the product cannot be added to the cart.
            ValidationError: If the product type does not match the provided type or
             if the product is variable and no attribute ID is provided.
        """
        product_id = data.get("product_id")
        product_type = data.get("product_type")
        attribute_id = data.get("attribute_id", None)

        product = (
            Product.objects.filter(id=product_id).prefetch_related("stock_item").first()
        )

        if not product:
            raise NotFound({"product_id": "Product not found " + str(product_id)})

        if product.status != Product.ProductStatus.PUBLISHED:
            raise PermissionDenied(
                {"product_id": "Product can not be added to cart " + str(product_id)}
            )

        if product.type != product_type:
            raise ValidationError(
                {
                    "product_id": f"Product with id {product_id} does not match the provided type {product_type}."
                }
            )

        if product.type == Product.ProductType.VARIABLE and not attribute_id:
            raise ValidationError(
                {"attribute_id": "Attribute ID is required for variable products"}
            )

        if product.type == Product.ProductType.VARIABLE:
            attribute = ProductAttribute.objects.filter(
                id=attribute_id, product=product
            ).first()

            if not attribute:
                raise NotFound(
                    {"attribute_id": "Attribute not found for the provided product"}
                )

            if not self.stock_validator.check_stock_item_stock(
                attribute.stock_item, data.get("quantity")
            ):
                calculated_available_stock = attribute.stock_item.stock
                if calculated_available_stock <= 0:
                    message = f'Производот "{product.title} - {attribute.title}" е распродаден.'
                else:
                    message = f'Имаме само {calculated_available_stock} од "{product.title} - {attribute.title}" на залиха.'

                extraDict = {
                    "product_id": product_id,
                    "attribute_id": attribute_id,
                    "quantity": data.get("quantity"),
                    "available_quantity": calculated_available_stock,
                    "message": message,
                }

                raise OutOfStockException(
                    data.get("quantity"),
                    calculated_available_stock,
                    extraDict,
                )

            return product, product_type, attribute, data.get("quantity")

        if not self.stock_validator.check_stock_item_stock(
            product.stock_item, data.get("quantity")
        ):
            calculated_available_stock = product.stock_item.stock
            if calculated_available_stock <= 0:
                message = f'Производот "{product.title}" е распродаден.'
            else:
                message = f'Имаме само {calculated_available_stock} од "{product.title}" на залиха.'

            extraDict = {
                "product_id": product_id,
                "quantity": data.get("quantity"),
                "available_quantity": calculated_available_stock,
                "message": message,
            }

            raise OutOfStockException(
                data.get("quantity"), calculated_available_stock, extraDict
            )

        return product, product_type, None, data.get("quantity")
