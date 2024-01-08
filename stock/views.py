from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from stock.serializers import ManageStockItemSerializer, StockItemSerializer
from .services.stock_item_service import StockItemService
from .utils import IsStockManager


class ManageStockItemView(APIView):
    permission_classes = [IsStockManager]

    def post(self, request):
        serializer = ManageStockItemSerializer(data=request.data)
        if serializer.is_valid():
            stock_item_service = StockItemService()
            stock_item = stock_item_service.manage_stock_item_by_action(serializer)
            return Response(
                StockItemSerializer(stock_item).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
