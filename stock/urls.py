from django.urls import path

from .views import ManageStockItemView

urlpatterns = [
    path("manage-stock-item/", ManageStockItemView.as_view(), name="stockitem-manage"),
]
