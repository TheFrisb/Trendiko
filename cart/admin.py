import nested_admin
from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet

from stock.models import ReservedStockItem
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


class ReservedStockItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        order_item = self.forms[0].cleaned_data["order_item"]
        reserved_quantity_sum = 0
        is_same_stock_item = True
        stock_check = {}

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                import_item = form.cleaned_data["import_item"]
                initial_quantity = form.cleaned_data["initial_quantity"]

                reserved_quantity_sum += initial_quantity

                if import_item in stock_check:
                    stock_check[import_item] += initial_quantity
                else:
                    stock_check[import_item] = initial_quantity

                if form.cleaned_data["import_item"].stock_item != order_item.stock_item:
                    raise forms.ValidationError(
                        f"The import item set for one of the reserved stock items '{form.cleaned_data["import_item"]}"
                        f" is not the same as the order item's '{order_item.stock_item}'"
                    )
        if reserved_quantity_sum != order_item.quantity:
            raise forms.ValidationError(
                f"The sum of reserved stock quantities '{reserved_quantity_sum}' does not match the order item quantity"
                f" '{order_item.quantity}'."
            )

        for import_item, reserved_quantity in stock_check.items():
            max_reservation = import_item.calculate_max_available_reservation()
            if reserved_quantity > max_reservation:
                raise forms.ValidationError(
                    f"The quantity '{reserved_quantity}' exceeds the maximum available reservation "
                    f"'{max_reservation}' for import item '{import_item}'."
                )


        self.quantity = reserved_quantity_sum



class OrderItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                product = form.cleaned_data["product"]
                stock_item = form.cleaned_data["stock_item"]
                attribute = form.cleaned_data["attribute"]

                if product.isVariable() and not attribute:
                    raise forms.ValidationError(
                        f"The field attribute must be populated for the variable product '{product.title}'"
                    )

                if product.isVariable() and attribute is not None:
                    if attribute.stock_item != stock_item:
                        raise forms.ValidationError(
                            f"The stock item you have selected is not correct for the attribute '{attribute.title}'"
                        )

                    if attribute.product.id != product.id:
                        raise forms.ValidationError(
                            f"The attribute '{attribute.title}' does not belong to the product {product.title}"
                        )

                if not product.isVariable() and stock_item != product.stock_item:
                    raise forms.ValidationError(
                        f"The stock item you have selected is not correct for the product '{product.title}'"
                    )

                if stock_item.available_stock < form.cleaned_data['quantity']:
                    raise forms.ValidationError(
                        f"Not enough ({form.cleaned_data['quantity']} stock for '{stock_item}'."
                    )




class ReservedStockItemInline(nested_admin.NestedTabularInline):
    model = ReservedStockItem
    extra = 1
    autocomplete_fields = ["import_item"]
    readonly_fields = ["quantity"]
    formset = ReservedStockItemFormSet


class ShippingDetailsInline(nested_admin.NestedStackedInline):  # Updated inheritance
    model = ShippingDetails
    extra = 0


class OrderItemInline(nested_admin.NestedTabularInline):
    model = OrderItem
    extra = 0
    inlines = [ReservedStockItemInline]
    formset = OrderItemFormSet
    autocomplete_fields = ["product", "stock_item", "attribute"]


@admin.register(Order)
class OrderAdmin(nested_admin.NestedModelAdmin):
    inlines = [OrderItemInline, ShippingDetailsInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'session_key', 'status', 'tracking_number')
        }),
        ('Pricing Details', {
            'fields': ('shipping_price', 'subtotal_price', 'total_price', 'has_free_shipping')
        }),
        ('Shipping & Invoicing', {
            'fields': ('exportable_date', 'pdf_invoice', 'mail_is_sent')
        }),
        ('Additional Info', {
            'fields': ('ip', 'user_agent')
        }),
    )
    readonly_fields = ['ip', 'user_agent', 'mail_is_sent', 'session_key',
                       'tracking_number', 'pdf_invoice', 'exportable_date']

    autocomplete_fields = ["user"]

    change_form_template = "admin/order/change_form.html"
    def save_related(self, request, form, formsets, change):
        """
        After saving the related formsets, call the recalculate_totals method.
        """
        super().save_related(request, form, formsets, change)
        print(form.instance.tracking_number)
        form.instance.generate_client_sale()
