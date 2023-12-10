from django.urls import path
from .views import CartItemView, CheckoutView

urlpatterns = [
    path("cart-item/", CartItemView.as_view(), name="cartitem-simple"),
    path("cart-item/<int:pk>/", CartItemView.as_view(), name="cartitem-update"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
