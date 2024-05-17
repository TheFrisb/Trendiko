from django.urls import path

from .api_views import ProductAPIView, ProductAttributeAPIView
from .views import (
    HomeView,
    ProductDetailView,
    CategoryListView,
    ThankYouDetailView,
    BrandPageDetailView,
    SearchView,
)

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category_page"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_page"),
    path(
        "thank-you/<str:tracking_number>/",
        ThankYouDetailView.as_view(),
        name="thank_you_page",
    ),
    path("brand/<slug:slug>/", BrandPageDetailView.as_view(), name="brand_page"),
    path("search/", SearchView.as_view(), name="search_page"),
    path("api/products/<int:pk>/", ProductAPIView.as_view(), name="product_api"),
    path(
        "api/product-attributes/<int:pk>/",
        ProductAttributeAPIView.as_view(),
        name="product_attribute_api",
    ),
]
