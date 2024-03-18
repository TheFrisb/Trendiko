from django.urls import path

from .views import feed_facebook_catalogue

urlpatterns = [
    path(
        "feed-facebook-catalogue/",
        feed_facebook_catalogue,
        name="feed-facebook-catalogue",
    ),
]
