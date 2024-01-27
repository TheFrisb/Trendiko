from django.http import Http404
from django.shortcuts import render

from shop.models import Category, Product


# Create your views here.


def home_view(request):
    categories = Category.objects.all()
    promotion_category = categories.filter(is_on_promotion=True).first()
    recommended_products = Product.objects.all().order_by("-created_at")[:4]
    free_shipping_products = Product.objects.filter(has_free_shipping=True).order_by(
        "-created_at"
    )[:4]

    if not promotion_category:
        promotion_category = categories.first()

    context = {
        "categories": categories,
        "promotion_category": promotion_category,
        "recommended_products": recommended_products,
        "free_shipping_products": free_shipping_products,
        "title": "Home",
    }

    return render(request, "shop/home.html", context)


def product_detail_view(request, slug):
    try:
        product = (
            Product.objects.prefetch_related("attributes", "category", "reviews")
            .select_related("category")
            .get(slug=slug, status=Product.ProductStatus.PUBLISHED)
        )
    except Product.DoesNotExist:
        raise Http404("Product does not exist or is not published.")

    categories = Category.objects.all()
    context = {
        "product": product,
        "title": product.title,
        "categories": categories,
        "product_misc_data": product.get_product_misc_data(),
    }
    return render(request, "shop/product_pages/main_product_page.html", context)
