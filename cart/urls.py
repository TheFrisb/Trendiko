from django.urls import path

from .views import CartItemView, CheckoutView, OrderItemView

urlpatterns = [
    path("cart-item/", CartItemView.as_view(), name="cartitem-add"),
    path("cart-item/<int:pk>/", CartItemView.as_view(), name="cartitem-update"),
    path("order-item/", OrderItemView.as_view(), name="orderitem-add"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
