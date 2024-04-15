from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Order
from common.exceptions import OutOfStockException
from shop_manager.serializers import (
    ChangeOrderStatusSerializer,
    RemoveAbandonedCartSerializer,
)
from shop_manager.utils import IsShopManagerPermission, IsAbandonedCartPermission


class ChangeOrderStatus(APIView):
    permission_classes = [IsShopManagerPermission]

    def post(self, request):
        serializer = ChangeOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data["order"]
            new_status = serializer.validated_data["new_status"]

            if (
                order.status == Order.OrderStatus.DELETED
                and new_status != Order.OrderStatus.DELETED
            ):
                order.exportable_date = now()

            order.status = new_status

            try:
                order.save()
            except ValueError as exc:
                exc_dict = exc.args[0]
                order_item = exc_dict["order_item"]
                message = f"Нема доволно на залиха за '{order_item.get_readable_name} - x{order_item.quantity}'."
                raise OutOfStockException(0, 0, {"message": message})

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveAbandonedCart(APIView):
    permission_class = [IsAbandonedCartPermission]

    def post(self, request):
        serializer = RemoveAbandonedCartSerializer(data=request.data)

        if serializer.is_valid():
            cart = serializer.validated_data["cart"]
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
