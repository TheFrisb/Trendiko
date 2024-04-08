from django.urls import path

from .api_views import MailSubscriptionView

urlpatterns = [
    path(
        "mail-subscription/", MailSubscriptionView.as_view(), name="mail-subscription"
    ),
]
