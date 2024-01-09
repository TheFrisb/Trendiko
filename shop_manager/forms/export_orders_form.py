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
        print(orders)
        return orders

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
