from django.http import FileResponse, HttpResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView
from weasyprint import HTML

from cart.models import Order
from stock.models import StockItem
from .forms.export_orders_form import ExportOrdersForm
from .forms.export_stock_information_form import ExportStockInformationForm
from .utils import (
    ShopManagerRequiredMixin,
    SidebarItemsMixin,
    StockManagerRequiredMixin,
    AnalyticsManagerRequiredMixin,
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
            Order.objects.filter(status=self.status)
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


class AnalyticsDashboard(AnalyticsManagerRequiredMixin, BaseDashboardView):
    model = None
    template_name = f"{dashboards_dir}/analytics.html"

    def get_queryset(self):
        # Fix
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Аналитика"
        return context


class GenerateOrderInvoice(ShopManagerRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        pdf_file = self.generate_pdf(request, order_id)
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="example.pdf"'
        return response

    def generate_pdf(self, request, order_id):
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

        if not order.barcode:
            order.generate_barcode()

        context = {
            "order": order,
            "order_items": order.order_items.all(),
            "shipping_details": order.shipping_details,
        }

        html_string = render_to_string("shop_manager/pdf_template.html", context)

        return HTML(
            string=html_string, base_url=request.build_absolute_uri()
        ).write_pdf()
