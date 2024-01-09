from django.urls import path

from .views import ManageStockItemView, StockItemDetailView

urlpatterns = [
    path("manage-stock-item/", ManageStockItemView.as_view(), name="stockitem-manage"),
    path(
        "stock-item/<str:sku>/", StockItemDetailView.as_view(), name="stock-item-detail"
    ),
]
