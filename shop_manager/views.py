from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from analytics.models import CampaignSummary, CampaignEntry
from cart.models import Order, Cart
from stock.models import StockItem
from .forms.export_invoices import ExportInvoicesForm
from .forms.export_orders_form import ExportOrdersForm
from .forms.export_stock_information_form import ExportStockInformationForm
from .utils import (
    ShopManagerRequiredMixin,
    SidebarItemsMixin,
    StockManagerRequiredMixin,
    AnalyticsManagerRequiredMixin,
    AbandonedCartsManagerRequiredMixin,
    ShopClientManagerRequiredMixin,
)

# Create your views here.
dashboards_dir = "shop_manager/dashboards"


class BaseDashboardView(SidebarItemsMixin, ListView):
    template_name = "shop_manager/base.html"


class ShopManagerHome(ShopManagerRequiredMixin, BaseDashboardView):
    model = Order
    template_name = f"{dashboards_dir}/orders.html"
    context_object_name = "orders"
    paginate_by = 24

    # catch post request from export orders form
    def post(self, request, *args, **kwargs):
        form = ExportOrdersForm(request.POST)
        if form.is_valid():
            return FileResponse(
                form.export_orders(), as_attachment=True, filename="orders.xlsx"
            )
        return self.get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.status = request.GET.get("status", Order.OrderStatus.PENDING)
        valid_statuses = [status[0] for status in Order.OrderStatus.choices]
        if self.status not in valid_statuses:
            self.status = Order.OrderStatus.PENDING

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Order.objects.filter(status=self.status, user__isnull=True)
            .order_by("-id")
            .prefetch_related(
                "order_items", "order_items__product", "order_items__attribute"
            )
            .select_related("shipping_details")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context[
            "title"
        ] = f"{dict(Order.OrderStatus.choices)[self.status]} нарачки".capitalize()
        context["export_orders_form"] = ExportOrdersForm()
        context["OrderStatuses"] = Order.OrderStatus
        context["url_param"] = f"status={self.status}"
        return context


class StockManagerHome(StockManagerRequiredMixin, BaseDashboardView):
    model = StockItem
    template_name = f"{dashboards_dir}/stock_items.html"
    context_object_name = "stock_items"
    paginate_by = 24

    def post(self, request, *args, **kwargs):
        form = ExportStockInformationForm(request.POST)
        return FileResponse(
            form.export_stock_imports_information(),
            as_attachment=True,
            filename="stock.xlsx",
        )

    def get_queryset(self):
        return StockItem.objects.filter().prefetch_related("importitem_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Контрола на залиха"
        context["template"] = "stock_items"
        return context


class ScanStock(StockManagerRequiredMixin, BaseDashboardView):
    model = StockItem
    template_name = f"{dashboards_dir}/scan_stock.html"

    def get_queryset(self):
        # Fix
        return StockItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Скенирај залиха"
        return context


class GenerateOrderInvoice(ShopManagerRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        pdf_file = self.fetch_pdf(request, order_id)
        filename = f"order_{order_id}_invoice.pdf"
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    def fetch_pdf(self, request, order_id):
        order = (
            Order.objects.filter(id=order_id)
            .prefetch_related(
                "order_items",
                "order_items__product",
                "order_items__attribute",
                "order_items__stock_item",
            )
            .select_related("shipping_details")
            .first()
        )

        if not order:
            raise Http404("Order does not exist")

        return order.pdf_invoice


class ExportInvoices(ShopManagerRequiredMixin, View):
    def post(self, request):
        form = ExportInvoicesForm(request.POST)
        if form.is_valid():
            return FileResponse(
                form.export_invoices(),
                as_attachment=True,
                filename="invoices.pdf",
            )
        return HttpResponse("Invalid form data", status=400)


class AbandonedCartsDashboard(AbandonedCartsManagerRequiredMixin, BaseDashboardView):
    model = Cart
    template_name = f"{dashboards_dir}/abandoned_carts.html"
    context_object_name = "orders"
    paginate_by = 24

    def get_queryset(self):
        return (
            Cart.objects.filter(
                status=Cart.CartStatus.ABANDONED, abandoned_cart_details__isnull=False
            )
            .select_related("abandoned_cart_details")
            .prefetch_related("cart_items")
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Abandoned Carts"
        return context


class ClientDashboard(ShopClientManagerRequiredMixin, BaseDashboardView):
    model = Order
    template_name = f"{dashboards_dir}/shop_client.html"
    context_object_name = "orders"
    paginate_by = 50

    def get_queryset(self, queryset=None):
        pk = self.kwargs.get("pk")

        test = (
            Order.objects.filter(user_id=pk)
            .prefetch_related(
                "order_items__product",
                "order_items__attribute",
                "order_items__reserved_stock_items",
                "order_items__reserved_stock_items__import_item",
            )
            .order_by("created_at")
        )

        return test


def test_pdf(request):
    return render(
        request,
        "shop_manager/accountant_pdf.html",
        context={"counter": 0, "current_date": "03.03.2001"},
    )


class FacebookAnalyticsDashboard(AnalyticsManagerRequiredMixin, BaseDashboardView):
    model = CampaignSummary
    context_object_name = "campaign_summaries"
    template_name = f"{dashboards_dir}/analytics/facebook_analytics_list.html"

    def get_queryset(self):
        return CampaignSummary.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Facebook Analytics"
        context["listable_items"] = self.object_list

        return context


class FacebookAnalyticsDetailDashboard:
    model = CampaignEntry
