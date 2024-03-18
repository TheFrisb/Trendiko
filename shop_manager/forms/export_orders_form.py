import io

import xlsxwriter
from django import forms

from cart.models import Order, OrderItem
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
        thank_you_offers = {}
        nabavki = {}
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
            worksheet.write(
                row, 4, order.shipping_details.municipality, centered_cell_format
            )
            worksheet.write(row, 5, order.shipping_details.phone, centered_cell_format)
            worksheet.write(row, 6, "ORDER FEES", centered_cell_format)
            worksheet.write(row, 7, order.total_price, centered_cell_format)
            worksheet.write(row, 8, order.get_shipping_method, centered_cell_format)

            product_titles = ""
            product_skus = ""
            quantity = 0
            cell_height = 15

            for order_item in order.order_items.all():
                product_titles += (
                    f"{order_item.product.title} x {order_item.quantity}\n"
                )
                product_skus += (
                    f"{order_item.stock_item.label} x {order_item.quantity}\n"
                )
                quantity += order_item.quantity
                cell_height += 15

                if order_item.promotion_type == OrderItem.PromotionType.THANK_YOU:
                    if order_item.stock_item.label in thank_you_offers:
                        thank_you_offers[
                            order_item.product.title
                        ] += order_item.quantity
                    else:
                        thank_you_offers[
                            order_item.stock_item.label
                        ] = order_item.quantity

                for reserved_item in order_item.reserved_stock_items.all():
                    if reserved_item.import_item.id in nabavki:
                        nabavki[reserved_item.import_item.id][
                            "quantity"
                        ] += reserved_item.quantity
                    else:
                        nabavki[reserved_item.import_item.id] = {
                            "quantity": reserved_item.quantity,
                            "stock_item": reserved_item.import_item.stock_item,
                            "import_item": reserved_item.import_item,
                        }

            worksheet.set_row(row, cell_height)
            worksheet.write(row, 9, product_titles, centered_cell_format)
            worksheet.write(row, 10, product_skus, centered_cell_format)
            worksheet.write(row, 11, f"X {quantity}", centered_cell_format)
            worksheet.write(row, 12, quantity, centered_cell_format)
            worksheet.write(
                row, 13, order.shipping_details.comment, centered_cell_format
            )

            row += 5

        worksheet.write(row, 0, "THANK YOU OFFERS", centered_cell_format)
        row += 1
        row, col = self.write_thank_you_headers(worksheet, centered_cell_format, row, 0)
        row += 1
        for label, quantity in thank_you_offers.items():
            worksheet.write(row, 0, label, centered_cell_format)
            worksheet.write(row, 1, quantity, centered_cell_format)
            row += 1

        stock_worksheet = workbook.add_worksheet("Stock")
        row, col = self.write_stock_headers(stock_worksheet, centered_cell_format, 0, 0)
        row += 1
        for import_id, data in nabavki.items():
            stock_worksheet.set_row(row, 94)
            image_path = data["stock_item"].thumbnail_loop_as_jpeg.path
            # absolute_image_path = os.path.join(settings.MEDIA_ROOT, relative_image_path)

            stock_worksheet.insert_image(
                row,
                0,
                image_path,
                {"x_scale": 0.5, "y_scale": 0.5},
            )
            stock_worksheet.write(
                row, 1, data["stock_item"].title, centered_cell_format
            )
            stock_worksheet.write(
                row, 2, data["stock_item"].label, centered_cell_format
            )
            stock_worksheet.write(row, 3, data["stock_item"].sku, centered_cell_format)
            stock_worksheet.write(row, 4, data["quantity"], centered_cell_format)
            stock_worksheet.write(
                row, 5, data["import_item"].price_no_vat, centered_cell_format
            )
            # write this field with formula of previous cell * this new cell
            stock_worksheet.write_formula(
                row,
                6,
                f"=E{row + 1} * F{row + 1}",
                centered_cell_format,
            )

            row += 1

        workbook.close()
        output.seek(0)

        return output

    def write_stock_headers(self, worksheet, format, row, col):
        headers = [
            "SLIKA",
            "IME NA ITEM",
            "LABEL",
            "SKU",
            "KOLICINA",
            "NABAVNA",
            "NABAVNA VKUPNO",
        ]

        for header in headers:
            worksheet.set_column(col, col, 30)
            worksheet.write(row, col, header, format)

            col += 1

        # set 0, 0 to width of 250px for image
        worksheet.set_column(0, 0, 17)

        return row, col

    def write_order_headers(self, worksheet, format, row, col):
        headers = [
            "DATA NA PORACKA",
            "IME I PREZIME",
            "ADRESA",
            "GRAD",
            "OPSTINA",
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

    def write_thank_you_headers(self, worksheet, format, row, col):
        headers = [
            "IME NA PRODUKT",
            "KOLICINA",
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
            Order.objects.filter(
                created_at__gte=from_date,
                created_at__lt=to_date,
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

        return orders
