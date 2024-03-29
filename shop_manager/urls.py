from django.urls import path

from .actions_views import ChangeOrderStatus
from .views import (
    ShopManagerHome,
    StockManagerHome,
    ScanStock,
    AnalyticsDashboard,
    GenerateOrderInvoice,
)

app_name = "shop_manager"
urlpatterns = [
    path("dashboard/", ShopManagerHome.as_view(), name="order_dashboard"),
    path(
        "dashboard/manage-stock-items/",
        StockManagerHome.as_view(),
        name="stock_dashboard",
    ),
    path("dashboard/scan-stock-items/", ScanStock.as_view(), name="scan_stock"),
    path(
        "dashboard/analytics-dashboard,",
        AnalyticsDashboard.as_view(),
        name="analytics_dashboard",
    ),
    path(
        "api/change-order-status/",
        ChangeOrderStatus.as_view(),
        name="change_order_status",
    ),
    path(
        "invoices/<int:order_id>/", GenerateOrderInvoice.as_view(), name="order_invoice"
    ),
]
