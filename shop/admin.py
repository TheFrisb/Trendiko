from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from facebook.admin import FacebookCampaignsInline
from .models import (
    Product,
    ProductAttribute,
    Category,
    Review,
    ProductImage,
    BrandPage,
    FrequentlyAskedQuestion,
)


# Register your models here.
class ProductAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=FilteredSelectMultiple(verbose_name="Categories", is_stacked=False),
    )

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")

        if type == Product.ProductType.VARIABLE:
            return

        stock_item = cleaned_data.get("stock_item")
        status = cleaned_data.get("status")

        if self.status_requires_stock_item(status) and not stock_item:
            raise ValidationError(
                "Stock item must be selected for Simple Products with status 'Published' or 'Out of Stock'"
            )

    def status_requires_stock_item(self, status):
        """
        Check if the status requires a stock item
        :param status: Product status
        :return: True if status requires stock item, False otherwise
        """
        if status != Product.ProductStatus.ARCHIVED:
            return True
        return False

    class Meta:
        model = Product
        fields = "__all__"


class FrequentlyAskedQuestionAdminForm(forms.ModelForm):
    # check if when saving in the admin, if Product is not selected, is_default is True
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        is_default = cleaned_data.get("is_default")
        if not product and not is_default:
            raise ValidationError(
                "Мора да биде одберано 'Стандардно прашање' ако не е одберан производот!"
            )

    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"


class FAQInline(admin.TabularInline):
    model = FrequentlyAskedQuestion
    extra = 0
    form = FrequentlyAskedQuestionAdminForm
    fields = ["question", "answer"]


class ProductAttributeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        attribute_types = set()
        for form in self.forms:
            if not form.cleaned_data:
                continue
            attribute_type = form.cleaned_data.get("type")
            attribute_types.add(attribute_type)

            # if attribute doesn't have a stock item assigned to it, raise an error
            if not form.cleaned_data.get("stock_item") and not form.cleaned_data.get(
                "DELETE"
            ):
                raise ValidationError("Stock item must be selected for each attribute.")

            if len(attribute_types) > 1:
                raise ValidationError("All attributes must be of the same type.")


class ProductAttributeInline(admin.TabularInline):
    autocomplete_fields = ["stock_item"]
    model = ProductAttribute
    extra = 0
    fields = [
        "thumbnail",
        "type",
        "title",
        "value",
        "sale_price",
        "regular_price",
        "stock_item",
    ]
    formset = ProductAttributeInlineFormSet

    class Media:
        js = ("admin/js/product_attribute.js",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    autocomplete_fields = ["stock_item"]
    list_display = [
        "title",
        "status",
        "type",
        "regular_price",
        "sale_price",
    ]
    list_filter = ["status", "type", "categories", "stock_item"]
    search_fields = ["title", "stock_item__sku", "stock_item__label"]
    inlines = [
        ProductImageInline,
        ProductAttributeInline,
        FAQInline,
        FacebookCampaignsInline,
    ]
    readonly_fields = ["slug"]

    class Meta:
        model = Product


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_filter = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    # group parent_css, div_css
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "promotion_text",
                    "promotion_image",
                    "is_on_promotion",
                    "is_default",
                    "max_discount",
                    "slug",
                )
            },
        ),
        (
            "CSS",
            {
                "classes": ("collapse",),
                "fields": ("banner_css", "headline_css", "discount_bar_css"),
            },
        ),
    )

    def delete_model(self, request, obj):
        if not obj.is_default:
            obj.delete()
        else:
            raise ValidationError("You can't delete the default category")

    class Meta:
        model = Category


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "name", "rating", "created_at"]
    list_filter = ["product", "name", "rating"]
    search_fields = ["product", "name"]

    class Meta:
        model = Review


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer"]
    list_filter = ["product", "is_default"]
    search_fields = ["question", "answer", "product__title"]
    autocomplete_fields = ["product"]
    form = FrequentlyAskedQuestionAdminForm

    class Meta:
        model = FrequentlyAskedQuestion


admin.site.register(BrandPage)
