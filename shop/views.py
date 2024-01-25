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
