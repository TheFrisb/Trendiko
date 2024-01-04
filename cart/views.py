from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.services.product_service import ProductService
from .serializers import (
    AddProductToCartSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
    ShippingDetailsSerializer,
)
from cart.services.cart_service import CartService
from cart.services.checkout_service import CheckoutService


class CartItemView(APIView):
    """
    API view for handling operations related to cart items.

    The POST method is used to add a product to the cart.
    The PUT method is used to update the quantity of a cart item.
    The DELETE method is used to remove a cart item from the cart."""

    def post(self, request):
        """
        Add a product to the cart or update its quantity if it's already in the cart.

        Args:
            request (Request): The request object containing the product and quantity.

        Returns:
            Response: The response object containing the cart item data or error message.
        """

        serializer = AddProductToCartSerializer(data=request.data)
        if serializer.is_valid():
            cart_service = CartService(request.cart, ProductService())
            cart_item = cart_service.add_product_to_cart(serializer.data)

            return Response(
                CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update the quantity of a cart item.

        Args:
            request (Request): The request object containing the new quantity.
            pk (int): The primary key of the cart item to be updated.

        Returns:
            Response: The response object containing the updated cart item data or error message.
        """

        serializer = UpdateCartItemSerializer(data=request.data)

        if serializer.is_valid():
            cart_service = CartService(request.cart, ProductService())

            cart_item = cart_service.update_cart_item(
                pk, serializer.validated_data["quantity"]
            )

            return Response(
                CartItemSerializer(cart_item).data, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Remove a cart item from the cart.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the cart item to be removed.

        Returns:
            Response: The response object with a status of 204 (No Content) or error message.
        """
        cart_service = CartService(request.cart, ProductService())

        cart_service.remove_from_cart(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    """
    API view for handling the checkout process.

    The POST method is used to initiate the checkout process.
    """

    def post(self, request):
        """
        Initiate the checkout process.

        Args:
            request (Request): The request object containing the shipping details.

        Returns:
            Response: The response object containing the order ID or error message.
        """
        serializer = ShippingDetailsSerializer(data=request.data)

        if serializer.is_valid():
            checkout_service = CheckoutService(request.cart)
            order = checkout_service.checkout(serializer.validated_data)

            return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
