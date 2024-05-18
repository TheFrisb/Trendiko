from django.urls import path

from facebook.insights import TotalAdSpend
from facebook.pixel_events_views import InitiateCheckout, ViewContent

app_name = "facebook"
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
    path(
        "insights/total-ad-spend/",
        TotalAdSpend.as_view(),
        name="retrieve_total_ad_spend",
    ),
]
