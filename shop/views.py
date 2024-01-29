from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import TemplateView, DetailView, ListView

from shop.mixins import FetchCategoriesMixin
from shop.models import Category, Product


# Create your views here.


class HomeView(FetchCategoriesMixin, TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = context.get("categories", Category.objects.none())
        promotion_category = categories.filter(is_on_promotion=True).first()

        if not promotion_category:
            promotion_category = categories.first()

        context.update(
            {
                "promotion_category": promotion_category,
                "recommended_products": Product.objects.all().order_by("-created_at")[
                    :4
                ],
                "free_shipping_products": Product.objects.filter(
                    has_free_shipping=True
                ).order_by("-created_at")[:4],
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
        try:
            product = queryset.get(slug=slug, status=Product.ProductStatus.PUBLISHED)
        except Product.DoesNotExist:
            raise Http404("Product does not exist or is not published.")

        return product

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["product_misc_data"] = self.object.get_product_misc_data()
        context["recommended_products"] = Product.objects.all().order_by("-created_at")[
            :4
        ]
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
