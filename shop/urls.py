from django.urls import path

from .views import HomeView, ProductDetailView, CategoryListView

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category_page"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_page"),
]
