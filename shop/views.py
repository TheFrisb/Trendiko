from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import TemplateView, DetailView, ListView

from cart.models import Order
from facebook.services.facebook_pixel import FacebookPixel
from shop.mixins import FetchCategoriesMixin
from shop.models import Category, Product, BrandPage


# Create your views here.


class HomeView(FetchCategoriesMixin, TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = context.get("categories", Category.objects.none())
        promotion_category = categories.filter(is_on_promotion=True).first()
        print(promotion_category.promotion_image)
        if not promotion_category:
            promotion_category = categories.first()

        context.update(
            {
                "promotion_category": promotion_category,
                "recommended_products_promotion": {
                    "products": Product.objects.all()
                    .filter(status=Product.ProductStatus.PUBLISHED)
                    .order_by("-created_at")[:6],
                    "redirect_slug": "site-proizvodi",
                },
                "free_shipping_promotion": {
                    "products": Product.objects.filter(
                        has_free_shipping=True,
                        status=Product.ProductStatus.PUBLISHED,
                    ).order_by("-created_at")[:4],
                    "redirect_slug": "besplatna-dostava",
                },
                "title": "Home",
            }
        )
        return context


class ProductDetailView(FetchCategoriesMixin, DetailView):
    model = Product
    template_name = "shop/product_pages/main_product_page.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        """Override get_object to include custom prefetching and selecting."""

        queryset = self.get_queryset().prefetch_related(
            "attributes", "reviews", "images"
        )

        slug = self.kwargs.get(self.slug_url_kwarg)
        fb = FacebookPixel(self.request)

        try:
            product = queryset.get(slug=slug, status=Product.ProductStatus.PUBLISHED)
            print(product.thumbnail.url)
            fb.view_content(product)
        except Product.DoesNotExist:
            raise Http404("Product does not exist or is not published.")

        return product

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["product_misc_data"] = self.object.get_product_misc_data()
        context["recommended_products_promotion"] = {
            "products": Product.objects.filter(
                status=Product.ProductStatus.PUBLISHED
            ).order_by("-created_at")[:4],
            "redirect_slug": "site-proizvodi",
        }

        context["show_call_button"] = True
        return context


class CategoryListView(FetchCategoriesMixin, ListView):
    model = Product
    template_name = "shop/category_page.html"
    context_object_name = "products"
    paginate_by = 24

    def get_queryset(self):
        products_queryset = Product.objects.filter(status="published").order_by(
            "created_at"
        )

        slug = self.kwargs.get("slug")
        try:
            self.category = Category.objects.prefetch_related(
                Prefetch("products", queryset=products_queryset)
            ).get(slug=slug)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")

        return self.category.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = self.category
        return context


class ThankYouDetailView(FetchCategoriesMixin, DetailView):
    model = Order
    template_name = "shop/thank_you_page.html"
    context_object_name = "order"
    slug_url_kwarg = "tracking_number"

    def get_object(self, queryset=None):
        queryset = (
            self.get_queryset()
            .prefetch_related(
                "order_items", "order_items__product", "order_items__attribute"
            )
            .select_related("shipping_details")
        )
        tracking_number = self.kwargs.get(self.slug_url_kwarg)
        try:
            order = queryset.get(tracking_number=tracking_number)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Thank You"
        context["promotion_product"] = self.object.make_thank_you_product()
        return context


class BrandPageDetailView(FetchCategoriesMixin, DetailView):
    model = BrandPage
    template_name = "shop/brand_page.html"
    context_object_name = "brand_page"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        try:
            brand_page = queryset.get(slug=slug)
        except BrandPage.DoesNotExist:
            raise Http404("Brand page does not exist")
        return brand_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context
