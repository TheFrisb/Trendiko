from common.models import GlobalCSS
from shop.models import Category, CartOffers


class FetchCategoriesMixin:
    def get_categories(self):
        return Category.objects.all().order_by("display_order")

    def get_css(self):
        return GlobalCSS.objects.filter().first()

    def get_banner(self):
        pass

    def get_cart_offers(self):
        return CartOffers.objects.all().order_by("display_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_categories()
        context["global_css"] = self.get_css()
        context["cart_offers"] = self.get_cart_offers()
        return context
