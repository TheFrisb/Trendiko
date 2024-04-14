from shop.models import Category


class FetchCategoriesMixin:
    def get_categories(self):
        return Category.objects.all().order_by("display_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.get_categories()
        return context
