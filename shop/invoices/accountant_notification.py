from django.template.loader import render_to_string
from weasyprint import HTML


class AccountantInvoicer:
    """
    Cool stuff
    """

    def generate_product_price_change_notification(
        self, old_item, new_item, base_url, as_base_64=True
    ):
        old_stock = old_item.stock_item.available_stock
        old_total = old_item.sale_price * old_stock
        new_stock = new_item.stock_item.available_stock
        new_total = new_item.sale_price * new_stock
        context = {
            "old_price": old_item.sale_price,
            "old_stock": old_stock,
            "old_total": old_total,
            "new_price": new_item.sale_price,
            "new_stock": new_stock,
            "new_total": new_total,
            "price_difference": abs(old_total - new_total),
            "product_title": new_item.get_product_title_for_accountant_invoice(),
        }

        html_string = render_to_string("shop_manager/accountant_pdf.html", context)
        return HTML(string=html_string, base_url=base_url).write_pdf()
