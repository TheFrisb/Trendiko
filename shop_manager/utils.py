from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from cart.models import Order
from shop_manager.forms.export_invoices import ExportInvoicesForm
from shop_manager.forms.export_orders_form import ExportOrdersForm
from shop_manager.forms.export_stock_information_form import ExportStockInformationForm


class ShopManagerBaseMixin:
    def is_shop_manager(self, request):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="shop_manager").exists()
        )


class ShopManagerRequiredMixin(ShopManagerBaseMixin, AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.is_shop_manager(request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())

    def get_login_url(self):
        next_url = self.request.get_full_path()
        return f"{resolve_url('admin:login')}?next={next_url}"


class StockManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="stock_manager").exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())

    def get_login_url(self):
        next_url = self.request.get_full_path()
        return f"{resolve_url('admin:login')}?next={next_url}"


class AnalyticsManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="analytics_manager").exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())

    def get_login_url(self):
        next_url = self.request.get_full_path()
        return f"{resolve_url('admin:login')}?next={next_url}"


# Permission class for DRF views
class IsShopManagerPermission(ShopManagerBaseMixin, BasePermission):
    def has_permission(self, request, view):
        if not self.is_shop_manager(request):
            raise PermissionDenied(detail="You must be a shop manager to access this.")
        return True


class SidebarItemsMixin:
    def get_sidebar_items(self):
        user = self.request.user
        sidebar_items = []

        if user.groups.filter(name="shop_manager").exists():
            sidebar_items.append(self.get_shop_manager_items())

        if user.groups.filter(name="stock_manager").exists():
            sidebar_items.append(self.get_stock_manager_items())

        if user.groups.filter(name="analytics_manager").exists():
            sidebar_items.append(self.get_analytics_manager_items())

        return sidebar_items

    def get_shop_manager_items(self):
        order_dashboard_url = reverse("shop_manager:order_dashboard")
        return {
            "title": "Shop Manager",
            "icon": "cart",
            "items": [
                {
                    "name": "Непотврдени порачки",
                    "url": f"{order_dashboard_url}?status={Order.OrderStatus.PENDING}",
                    "icon": "hourglass",
                },
                {
                    "name": "Потврдени порачки",
                    "url": f"{order_dashboard_url}?status={Order.OrderStatus.CONFIRMED}",
                    "icon": "check",
                },
                {
                    "name": "Избришани порачки",
                    "url": f"{order_dashboard_url}?status={Order.OrderStatus.DELETED}",
                    "icon": "trash",
                },
            ],
            "forms": [
                {
                    "title": "Export orders:",
                    "form": ExportOrdersForm(),
                    "action": reverse("shop_manager:order_dashboard"),
                    "method": "POST",
                    "button_text": "Export orders",
                },
                {
                    "title": "Export invoices:",
                    "form": ExportInvoicesForm(),
                    "action": reverse("shop_manager:export-invoices"),
                    "method": "POST",
                    "button_text": "Export invoices",
                },
            ],
        }

    def get_stock_manager_items(self):
        stock_dashboard_url = reverse("shop_manager:stock_dashboard")
        return {
            "title": "Stock Manager",
            "icon": "layers",
            "items": [
                {"name": "Залиха", "url": stock_dashboard_url, "icon": "sliders"},
                {
                    "name": "Скенири продукти",
                    "url": reverse("shop_manager:scan_stock"),
                    "icon": "scan",
                },
                {
                    "name": "Внеси увоз",
                    "url": reverse("admin:stock_import_add"),
                    "icon": "pencil",
                },
            ],
            "forms": [
                {
                    "title": "Export stock import:",
                    "form": ExportStockInformationForm(),
                    "action": reverse("shop_manager:stock_dashboard"),
                    "method": "POST",
                    "button_text": "Export stock imports",
                }
            ],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar_items"] = self.get_sidebar_items()
        return context

    def get_analytics_manager_items(self):
        analytics_dashboard_url = reverse("shop_manager:analytics_dashboard")
        return {
            "title": "Analytics",
            "icon": "scatter-chart",
            "items": [
                {
                    "name": "Daily rows",
                    "url": analytics_dashboard_url,
                    "icon": "line-chart",
                },
            ],
        }
