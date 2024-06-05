import io

import xlsxwriter
from django import forms

from cart.models import Order, OrderItem
from common.utils import make_timezone_aware


class Nabavki:
    def __init__(self):
        self.online_orders = {}
        self.offline_orders = {}
        self.total_nabavki = {}

    def add_nabavka(self, import_item, stock_item, quantity, is_online):
        if is_online:
            if import_item.id in self.online_orders:
                self.online_orders[import_item.id]["quantity"] += quantity
            else:
                self.online_orders[import_item.id] = {
                    "quantity": quantity,
                    "stock_item": stock_item,
                    "import_item": import_item,
                }
        else:
            if import_item.id in self.offline_orders:
                self.offline_orders[import_item.id]["quantity"] += quantity
            else:
                self.offline_orders[import_item.id] = {
                    "quantity": quantity,
                    "stock_item": stock_item,
                    "import_item": import_item,
                }

        if import_item.id in self.total_nabavki:
            self.total_nabavki[import_item.id]["quantity"] += quantity
        else:
            self.total_nabavki[import_item.id] = {
                "quantity": quantity,
                "stock_item": stock_item,
                "import_item": import_item,
            }


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
        # BIG YIKES BUT I"M TOO LAZY AT D MOMENT TO SPEND MORE THAN 2 MINS ON THIS
        nabavki = Nabavki()
        online_orders, offline_orders = self.get_orders()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Online")

        centered_cell_format = workbook.add_format()
        centered_cell_format.set_align("center")
        centered_cell_format.set_align("vcenter")

        row, col = self.write_order_headers(worksheet, centered_cell_format, 0, 0)
        row += 1
        thank_you_offers = {}
        for order in online_orders:
            worksheet.write(
                row, 0, order.created_at.strftime("%d-%m-%Y"), centered_cell_format
            )
            worksheet.write(row, 1, order.make_barcode_content(), centered_cell_format)
            try:
                worksheet.write(
                    row, 2, order.shipping_details.full_name, centered_cell_format
                )
                worksheet.write(
                    row, 3, order.shipping_details.address, centered_cell_format
                )
                worksheet.write(
                    row, 4, order.shipping_details.city, centered_cell_format
                )
                worksheet.write(
                    row, 5, order.shipping_details.municipality, centered_cell_format
                )
                worksheet.write(
                    row, 6, order.shipping_details.phone, centered_cell_format
                )
            except order._meta.model.shipping_details.RelatedObjectDoesNotExist:
                worksheet.write(row, 2, order.user.name, centered_cell_format)
                worksheet.write(row, 4, order.user.city, centered_cell_format)
                worksheet.write(row, 6, order.user.phone, centered_cell_format)

            worksheet.write(row, 7, "ORDER FEES", centered_cell_format)
            worksheet.write(row, 8, order.total_price, centered_cell_format)
            worksheet.write(row, 9, order.get_shipping_method, centered_cell_format)

            product_titles = ""
            product_skus = ""
            quantity = 0
            cell_height = 15

            for order_item in order.order_items.all():
                product_titles += (
                    f"{order_item.get_readable_name} x {order_item.quantity} "
                )
                product_skus += (
                    f"{order_item.stock_item.label} x {order_item.quantity} "
                )
                quantity += order_item.quantity
                cell_height += 15

                if order_item.promotion_type == OrderItem.PromotionType.THANK_YOU:
                    if order_item.stock_item.label in thank_you_offers:
                        thank_you_offers[
                            order_item.stock_item.label
                        ] += order_item.quantity
                    else:
                        thank_you_offers[
                            order_item.stock_item.label
                        ] = order_item.quantity

                for reserved_item in order_item.reserved_stock_items.all():
                    nabavki.add_nabavka(
                        import_item=reserved_item.import_item,
                        stock_item=reserved_item.import_item.stock_item,
                        quantity=reserved_item.quantity,
                        is_online=True,
                    )

            worksheet.set_row(row, cell_height)
            worksheet.write(row, 10, product_titles, centered_cell_format)
            worksheet.write(row, 11, product_skus, centered_cell_format)
            worksheet.write(row, 12, f"X {quantity}", centered_cell_format)
            worksheet.write(row, 13, quantity, centered_cell_format)
            worksheet.write(row, 14, "None")

            row += 1

        row += 5

        worksheet.write(row, 0, "NABAVKI", centered_cell_format)
        row += 1

        for import_id, data in nabavki.online_orders.items():
            worksheet.write(row, 0, data["stock_item"].label, centered_cell_format)
            worksheet.write(row, 1, data["quantity"], centered_cell_format)
            worksheet.write(
                row, 2, data["import_item"].price_vat_and_customs, centered_cell_format
            )
            worksheet.write_formula(
                row,
                3,
                f"=B{row + 1} * C{row + 1}",
                centered_cell_format,
            )

            row += 1

        row += 5
        worksheet.write(row, 0, "THANK YOU OFFERS", centered_cell_format)
        row += 1
        row, col = self.write_thank_you_headers(worksheet, centered_cell_format, row, 0)
        row += 1
        for label, quantity in thank_you_offers.items():
            worksheet.write(row, 0, label, centered_cell_format)
            worksheet.write(row, 1, quantity, centered_cell_format)
            row += 1

        offline_worksheet = workbook.add_worksheet("Offline")
        row, col = self.write_order_headers(
            offline_worksheet, centered_cell_format, 0, 0
        )
        row += 1
        for order in offline_orders:
            offline_worksheet.write(
                row, 0, order.created_at.strftime("%d-%m-%Y"), centered_cell_format
            )
            offline_worksheet.write(
                row, 1, order.make_barcode_content(), centered_cell_format
            )
            try:
                offline_worksheet.write(
                    row, 2, order.shipping_details.full_name, centered_cell_format
                )
                offline_worksheet.write(
                    row, 3, order.shipping_details.address, centered_cell_format
                )
                offline_worksheet.write(
                    row, 4, order.shipping_details.city, centered_cell_format
                )
                offline_worksheet.write(
                    row, 5, order.shipping_details.municipality, centered_cell_format
                )
                offline_worksheet.write(
                    row, 6, order.shipping_details.phone, centered_cell_format
                )
            except order._meta.model.shipping_details.RelatedObjectDoesNotExist:
                offline_worksheet.write(row, 2, order.user.name, centered_cell_format)
                offline_worksheet.write(row, 4, order.user.city, centered_cell_format)
                offline_worksheet.write(row, 6, order.user.phone, centered_cell_format)

            offline_worksheet.write(row, 7, "ORDER FEES", centered_cell_format)
            offline_worksheet.write(row, 8, order.total_price, centered_cell_format)
            offline_worksheet.write(
                row, 9, order.get_shipping_method, centered_cell_format
            )

            product_titles = ""
            product_skus = ""
            quantity = 0
            cell_height = 15

            for order_item in order.order_items.all():
                product_titles += (
                    f"{order_item.get_readable_name} x {order_item.quantity} "
                )
                product_skus += (
                    f"{order_item.stock_item.label} x {order_item.quantity} "
                )
                quantity += order_item.quantity
                cell_height += 15

                for reserved_item in order_item.reserved_stock_items.all():
                    nabavki.add_nabavka(
                        import_item=reserved_item.import_item,
                        stock_item=reserved_item.import_item.stock_item,
                        quantity=reserved_item.quantity,
                        is_online=False,
                    )

            offline_worksheet.set_row(row, cell_height)
            offline_worksheet.write(row, 10, product_titles, centered_cell_format)
            offline_worksheet.write(row, 11, product_skus, centered_cell_format)
            offline_worksheet.write(row, 12, f"X {quantity}", centered_cell_format)
            offline_worksheet.write(row, 13, quantity, centered_cell_format)
            offline_worksheet.write(row, 14, "None")

            row += 1

        row += 5

        offline_worksheet.write(row, 0, "NABAVKI", centered_cell_format)
        row += 1

        for import_id, data in nabavki.offline_orders.items():
            offline_worksheet.write(
                row, 0, data["stock_item"].label, centered_cell_format
            )
            offline_worksheet.write(row, 1, data["quantity"], centered_cell_format)
            offline_worksheet.write(
                row, 2, data["import_item"].price_vat_and_customs, centered_cell_format
            )
            offline_worksheet.write_formula(
                row,
                3,
                f"=B{row + 1} * C{row + 1}",
                centered_cell_format,
            )

            row += 1

        stock_worksheet = workbook.add_worksheet("Stock")
        row, col = self.write_stock_headers(stock_worksheet, centered_cell_format, 0, 0)
        row += 1
        for import_id, data in nabavki.total_nabavki.items():
            stock_worksheet.set_row(row, 94)
            if data["stock_item"].thumbnail.name:
                image_path = data["stock_item"].thumbnail_loop_as_jpeg.path

                stock_worksheet.insert_image(
                    row,
                    0,
                    image_path,
                    {"x_scale": 0.5, "y_scale": 0.5},
                )
            else:
                stock_worksheet.write(row, 0, "No image", centered_cell_format)
            stock_worksheet.write(
                row, 1, data["stock_item"].title, centered_cell_format
            )
            stock_worksheet.write(
                row, 2, data["stock_item"].label, centered_cell_format
            )
            stock_worksheet.write(row, 3, data["stock_item"].sku, centered_cell_format)
            stock_worksheet.write(row, 4, data["quantity"], centered_cell_format)
            stock_worksheet.write(
                row, 5, data["import_item"].price_vat_and_customs, centered_cell_format
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
            "BARCODE",
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

        online_orders = (
            Order.objects.filter(
                exportable_date__gte=from_date,
                exportable_date__lt=to_date,
                status__in=[Order.OrderStatus.PENDING, Order.OrderStatus.CONFIRMED],
                user=None,
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

        offline_orders = (
            Order.objects.filter(
                exportable_date__gte=from_date,
                exportable_date__lt=to_date,
                status__in=[Order.OrderStatus.PENDING, Order.OrderStatus.CONFIRMED],
                user__isnull=False,
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

        return online_orders, offline_orders
