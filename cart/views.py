import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.services.cart_service import CartService
from cart.services.checkout_service import CheckoutService
from facebook.services.facebook_pixel import FacebookPixel
from shop.services.product_service import ProductService
from .serializers import (
    AddProductToCartSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
    ShippingDetailsSerializer,
    CartSerializer,
    OrderSerializer,
    AddOrderItemToOrderSerializer,
    OrderItemSerializer,
    AbandonedCartDetailsSerializer,
)


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

            try:
                fb_pixel = FacebookPixel(request)
                fb_pixel.add_to_cart(cart_item)
            except Exception as e:
                logging.error(
                    f"[Facebook Pixel] Error when sending add to cart event: {e}"
                )

            return Response(
                CartItemSerializer(cart_item).data, status=status.HTTP_200_OK
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
        request.cart.refresh_from_db()

        return Response(CartSerializer(request.cart).data, status=status.HTTP_200_OK)


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
            checkout_service = CheckoutService(request)
            order = checkout_service.checkout(serializer.validated_data)

            try:
                fb_pixel = FacebookPixel(request)
                fb_pixel.purchase(order)
            except Exception as e:
                logging.error(
                    f"[Facebook Pixel] Error when sending checkout event: {e}"
                )

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemView(APIView):
    """
    API view for handling operations related to order items.

    The GET method is used to retrieve the order items of a specific order.
    """

    def post(self, request):
        serializer = AddOrderItemToOrderSerializer(data=request.data)

        if serializer.is_valid():
            checkout_service = CheckoutService(request)
            order_item = checkout_service.add_order_item_to_existing_order(
                serializer.validated_data
            )

            return Response(
                OrderItemSerializer(order_item).data, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AbandonedCartView(APIView):
    """
    API view for handling abandoned carts.

    The GET method is used to retrieve the abandoned carts.
    """

    def post(self, request):
        serializer = AbandonedCartDetailsSerializer(data=request.data)
        if serializer.is_valid():
            cart_service = CartService(request.cart, ProductService())
            cart_service.save_abandoned_cart_details(serializer.validated_data)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
