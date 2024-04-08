from django.contrib import admin

from .models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
    ShippingDetails,
    AbandonedCartDetails,
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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    filter_horizontal = ["reserved_stock_items"]
    readonly_fields = ["reserved_stock_items"]


class ShippingDetailsInline(admin.StackedInline):
    model = ShippingDetails
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ShippingDetailsInline]
    readonly_fields = ["ip", "user_agent"]

    change_form_template = "admin/order/change_form.html"
