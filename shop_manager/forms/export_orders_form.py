import io

import xlsxwriter
from django import forms

from cart.models import Order
from common.utils import make_timezone_aware


class ExportOrdersForm(forms.Form):
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

    def export_orders(self):
        orders = self.get_orders()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet()

        centered_cell_format = workbook.add_format()
        centered_cell_format.set_align("center")
        centered_cell_format.set_align("vcenter")

        row, col = self.write_order_headers(worksheet, centered_cell_format, 0, 0)

        row += 1

        for order in orders:
            worksheet.write(
                row, 0, order.created_at.strftime("%d-%m-%Y"), centered_cell_format
            )
            worksheet.write(
                row, 1, order.shipping_details.full_name, centered_cell_format
            )
            worksheet.write(
                row, 2, order.shipping_details.address, centered_cell_format
            )
            worksheet.write(row, 3, order.shipping_details.city, centered_cell_format)
            worksheet.write(row, 4, order.shipping_details.phone, centered_cell_format)
            worksheet.write(row, 5, "ORDER FEES", centered_cell_format)  # order.fees
            worksheet.write(row, 6, order.total_price, centered_cell_format)
            worksheet.write(row, 7, order.get_shipping_method, centered_cell_format)

            product_titles = ""
            product_skus = ""
            quantity = 0
            cell_height = 15

            for order_item in order.order_items.all():
                product_titles += (
                    f"{order_item.product.title} x {order_item.quantity}\n"
                )
                product_skus += f"#product_sku x {order_item.quantity}\n"
                quantity += order_item.quantity
                cell_height += 15

            worksheet.set_row(row, cell_height)
            worksheet.write(row, 8, product_titles, centered_cell_format)
            worksheet.write(row, 9, product_skus, centered_cell_format)
            worksheet.write(row, 10, f"X {quantity}", centered_cell_format)
            worksheet.write(row, 11, quantity, centered_cell_format)
            worksheet.write(
                row, 12, order.shipping_details.comment, centered_cell_format
            )

            row += 1

        workbook.close()
        output.seek(0)

        return output

    def write_order_headers(self, worksheet, format, row, col):
        headers = [
            "DATA NA PORACKA",
            "IME I PREZIME",
            "ADRESA",
            "GRAD",
            "TELEFON",
            "FEES",
            "VKUPNO",
            "DOSTAVA",
            "IME NA PRODUKT",
            "LABEL",
            "X KOLICINA",
            "KOLICINA",
            "KOMENTAR",
        ]

        for header in headers:
            worksheet.set_column(col, col, 30)
            worksheet.write(row, col, header, format)

            col += 1

        return row, col

    def get_orders(self):
        from_date = make_timezone_aware(self.cleaned_data["from_date"])
        to_date = make_timezone_aware(self.cleaned_data["to_date"])
        orders = (
            Order.objects.filter(created_at__gte=from_date, created_at__lt=to_date)
            .prefetch_related(
                "order_items", "order_items__product", "order_items__attribute"
            )
            .select_related("shipping_details")
        )

        return orders
