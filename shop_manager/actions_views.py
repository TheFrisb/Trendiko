from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop_manager.serializers import ChangeOrderStatusSerializer
from shop_manager.utils import IsShopManagerPermission


class ChangeOrderStatus(APIView):
    permission_classes = [IsShopManagerPermission]

    def post(self, request):
        serializer = ChangeOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data["order"]
            order.status = serializer.validated_data["new_status"]
            order.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
