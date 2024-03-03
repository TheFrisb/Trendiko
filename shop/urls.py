from django.urls import path

from .views import HomeView, ProductDetailView, CategoryListView, BrandPageDetailView

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category_page"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_page"),
    path("brand/<slug:slug>/", BrandPageDetailView.as_view(), name="brand_page"),
    path("thank-you/<str:tracking_number>/", HomeView.as_view(), name="thank_you_page"),
]
