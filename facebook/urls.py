from django.urls import path

from facebook.pixel_events_views import InitiateCheckout, ViewContent

urlpatterns = [
    path(
        "pixel/initiate-checkout/",
        InitiateCheckout.as_view(),
        name="initiatecheckout",
    ),
    path(
        "pixel/view-content/<str:product_slug>/",
        ViewContent.as_view(),
        name="viewcontent",
    ),
]
