from django.urls import path

from .actions_views import ChangeOrderStatus, RemoveAbandonedCart
from .views import (
    ShopManagerHome,
    StockManagerHome,
    ScanStock,
    FacebookAnalyticsDashboard,
    FacebookAnalyticsDetailDashboard,
    GenerateOrderInvoice,
    ExportInvoices,
    AbandonedCartsDashboard,
    test_pdf,
    ClientDashboard,
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
        "dashboard/analytics/facebook-campaigns/",
        FacebookAnalyticsDashboard.as_view(),
        name="analytics_dashboard",
    ),
    path(
        "dashboard/analytics/facebook-campaigns/<str:slug>/",
        FacebookAnalyticsDetailDashboard.as_view(),
        name="facebook_campaign_detail_view",
    ),
    path(
        "dashboard/abandoned-carts/",
        AbandonedCartsDashboard.as_view(),
        name="abandoned_carts_dashboard",
    ),
    path(
        "dashboard/clients/<int:pk>/",
        ClientDashboard.as_view(),
        name="client_dashboard",
    ),
    path(
        "api/change-order-status/",
        ChangeOrderStatus.as_view(),
        name="change_order_status",
    ),
    path(
        "api/remove-abandoned-cart/",
        RemoveAbandonedCart.as_view(),
        name="remove_abandoned_cart",
    ),
    path(
        "invoices/<int:order_id>/", GenerateOrderInvoice.as_view(), name="order_invoice"
    ),
    path("invoices/export/", ExportInvoices.as_view(), name="export-invoices"),
    path("test-pdf/", test_pdf),
]
