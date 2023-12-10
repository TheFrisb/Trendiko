from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, ShippingDetails


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class ShippingDetailsInline(admin.StackedInline):
    model = ShippingDetails
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ShippingDetailsInline]
