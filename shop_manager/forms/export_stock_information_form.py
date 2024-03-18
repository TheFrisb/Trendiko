import io

import xlsxwriter
from django import forms

from stock.models import Import


class ExportStockInformationForm(forms.Form):
    def export_stock_imports_information(self):
        stock_imports = self.get_imports()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        centered_cell_format = workbook.add_format()
        centered_cell_format.set_align("center")
        centered_cell_format.set_align("vcenter")

        for stock_import in stock_imports:
            worksheet = workbook.add_worksheet(
                f"{stock_import.title} - {stock_import.created_at.strftime('%d-%m-%Y')}"
            )
            row, col = self.write_headers(worksheet, centered_cell_format, 0, 0)

            row += 1

            for import_item in stock_import.importitem_set.all():
                worksheet.write(row, 0, import_item.stock_item.title)
                worksheet.write(row, 1, import_item.stock_item.label)
                worksheet.write(row, 2, import_item.stock_item.sku)
                worksheet.write(row, 3, import_item.quantity)
                worksheet.write(row, 4, import_item.stock_item.stock)
                worksheet.write(row, 5, import_item.reserved_stock)
                worksheet.write(row, 6, import_item.price_no_vat)
                worksheet.write(row, 7, import_item.price_vat)
                worksheet.write(row, 8, import_item.price_vat_and_customs)

                row += 1

        workbook.close()
        output.seek(0)

        return output

    def get_imports(self):
        return Import.objects.all().prefetch_related(
            "importitem_set", "importitem_set__stock_item"
        )

    def write_headers(self, worksheet, format, row, col):
        headers = [
            "UVOZEN PRODUKT IME",
            "UVOZEN PRODUKT LABEL",
            "UVOZEN PRODUKT SKU",
            "UVOZENA KOLICINA",
            "MOMENTALNA ZALIHA",
            "REZERVIRANA ZALIHA",
            "CENA BEZ DDV",
            "CENA SO DDV",
            "CENA SO DDV I CARINA",
        ]

        for header in headers:
            worksheet.set_column(col, col, 30)
            worksheet.write(row, col, header, format)

            col += 1

        return row, col
