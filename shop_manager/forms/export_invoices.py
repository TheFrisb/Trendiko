import os
import tempfile

import PyPDF2
from PyPDF2 import PdfWriter
from django import forms

from cart.models import Order
from common.utils import make_timezone_aware


class ExportInvoicesForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "dateInput",
                "placeholder": "Select a date",
                "required": "required",
            }
        )
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "dateInput",
                "placeholder": "Select a date",
                "required": "required",
            }
        )
    )

    def export_invoices(self, base_url):
        orders = self.get_orders()

        pdf_files = []
        combined_pdf = tempfile.NamedTemporaryFile(delete=False)

        with tempfile.TemporaryDirectory() as temp_dir:
            for order in orders:
                file_name = f"{order.id}.pdf"
                path = os.path.join(temp_dir, file_name)
                pdf_file = order.generate_invoice_pdf(base_url=base_url, write_to=path)
                pdf_files.append(pdf_file)

            self.merge_pdfs(pdf_files, combined_pdf.name)

        return open(combined_pdf.name, "rb")

    def get_orders(self):
        from_date = make_timezone_aware(self.cleaned_data["from_date"])
        to_date = make_timezone_aware(self.cleaned_data["to_date"])

        return (
            Order.objects.filter(
                created_at__gte=from_date,
                created_at__lte=to_date,
                status__in=[Order.OrderStatus.PENDING, Order.OrderStatus.CONFIRMED],
            )
            .prefetch_related(
                "order_items",
                "order_items__product",
                "order_items__attribute",
                "shipping_details",
                "order_items__reserved_stock_items",
                "order_items__reserved_stock_items__import_item",
                "order_items__reserved_stock_items__import_item__stock_item",
            )
            .select_related("shipping_details")
        )

    def merge_pdfs(self, pdf_paths, output_path):
        pdf_writer = PdfWriter()

        for path in pdf_paths:
            with open(path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in range(
                    len(pdf_reader.pages)
                ):  # Updated to use len(reader.pages)
                    pdf_writer.add_page(pdf_reader.pages[page])

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)