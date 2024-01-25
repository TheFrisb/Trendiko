from django.urls import path

from .views import home_view

app_name = "shop"

urlpatterns = [
    path("", home_view, name="home"),
    path("category/<slug:slug>/", home_view, name="category_page"),
    path("product/<slug:slug>/", home_view, name="product_page"),
]
