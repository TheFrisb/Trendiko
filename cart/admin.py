from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from common.exceptions import OutOfStockException
from shop.models import Product
from .models import (
    Cart,
    CartItem,
    AbandonedCartDetails,
    OrderItem,
    ShippingDetails,
    Order,
)


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class AbandonedCartDetailsInline(admin.StackedInline):
    model = AbandonedCartDetails
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, AbandonedCartDetailsInline]


# class ShippingDetailsInline(admin.StackedInline):
#     model = ShippingDetails
#     extra = 0
#
#
# class ReservedStockItemInline(admin.TabularInline):
#     model = ReservedStockItem
#     extra = 1
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     inlines = [ReservedStockItemInline]
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInline, ShippingDetailsInline]
#     readonly_fields = ["ip", "user_agent", "exportable_date"]
#
#     change_form_template = "admin/order/change_form.html"


class OrderItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if (
                form.cleaned_data
                and not form.cleaned_data.get("DELETE", False)
                and not form.cleaned_data["id"]
            ):
                product = form.cleaned_data.get("product", None)
                attribute = form.cleaned_data.get("attribute", None)

                if not product and not attribute:
                    raise ValidationError("You must select a product or an attribute")

                if product and attribute:
                    raise ValidationError(
                        "You can't select both a product and a variable product"
                    )
                if product:
                    form.cleaned_data["stock_item"] = product.stock_item
                elif attribute:
                    form.cleaned_data["stock_item"] = attribute.stock_item
                    form.cleaned_data["product"] = attribute.product
                    form.cleaned_data["type"] = Product.ProductType.VARIABLE

                if (
                    form.cleaned_data["stock_item"].available_stock
                    < form.cleaned_data["quantity"]
                ):
                    raise ValidationError(
                        f"Only {form.cleaned_data['stock_item'].available_stock} items are available for {form.cleaned_data['stock_item']}"
                    )

    # if creating new orderItems, use .reserve_stock_for_order_item() to reserve the stock with transaction.atomic

    def save_new(self, form, commit=True):
        order_item = super().save_new(form, commit=False)
        order_item.stock_item = form.cleaned_data["stock_item"]
        order_item.product = form.cleaned_data["product"]

        order_item.type = form.cleaned_data.get("type", Product.ProductType.SIMPLE)

        if commit:
            order_item.save()
            try:
                order_item.reserve_stock_for_order_item()
            except OutOfStockException as e:
                message = f"Имаме само {e.available_quantity} на залиха"
                raise ValidationError(message)
        return order_item


class ShippingDetailsInline(admin.StackedInline):  # Updated inheritance
    model = ShippingDetails
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    formset = OrderItemFormSet
    autocomplete_fields = ["product", "stock_item", "attribute"]
    fields = ["product", "attribute", "quantity", "price", "rabat"]

    class Media:
        js = ("admin/js/order_item_inline.js",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ShippingDetailsInline]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("user", "status", "tracking_number")},
        ),
        (
            "Pricing Details",
            {
                "fields": (
                    "shipping_price",
                    "subtotal_price",
                    "total_price",
                    "has_free_shipping",
                    "generate_pdf_invoice",
                )
            },
        ),
    )
    readonly_fields = [
        "ip",
        "user_agent",
        "mail_is_sent",
        "session_key",
        "tracking_number",
        "pdf_invoice",
        "exportable_date",
    ]

    autocomplete_fields = ["user"]

    change_form_template = "admin/order/change_form.html"

    def save_related(self, request, form, formsets, change):
        """
        After saving the related formsets, call the recalculate_totals method.
        """
        super().save_related(request, form, formsets, change)

        form.instance.generate_client_sale()
