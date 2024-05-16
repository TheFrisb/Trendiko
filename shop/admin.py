from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html

from facebook.admin import FacebookCampaignsInline
from .models import (
    Product,
    ProductAttribute,
    Category,
    Review,
    ProductImage,
    BrandPage,
    FrequentlyAskedQuestion,
    ShopClient,
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
    list_display = ["title", "sale_price", "get_stock_item_stock"]
    list_filter = ["status", "type", "categories", "stock_item"]
    search_fields = ["title", "stock_item__sku", "stock_item__label"]
    inlines = [
        ProductImageInline,
        ProductAttributeInline,
        FAQInline,
        FacebookCampaignsInline,
    ]
    readonly_fields = ["slug"]

    def get_stock_item_stock(self, obj):
        return obj.stock_item.stock if obj.stock_item else None

    get_stock_item_stock.short_description = "Stock"
    get_stock_item_stock.admin_order_field = "stock_item__stock"

    # def save_model(self, request, obj, form, change):
    #     if change and not obj.isVariable():
    #         old_obj = Product.objects.get(id=obj.id)
    #
    #         if old_obj.sale_price != obj.sale_price:
    #             accountant_invoicer = AccountantInvoicer()
    #             sendgrid_client = SendGridClient()
    #
    #             pdf = accountant_invoicer.generate_product_price_change_notification(
    #                 old_obj, obj, request.build_absolute_uri()
    #             )
    #
    #             sendgrid_client.send_mail(
    #                 [
    #                     "lilanikolova@yahoo.com",
    #                     "info@trendiko.mk",
    #                     "thefrisb@gmail.com",
    #                 ],
    #                 f"{obj.get_product_title_for_accountant_invoice()} - Промена на цена",
    #                 "<strong>Во attachment</strong>",
    #                 pdf,
    #             )
    #
    #     super().save_model(request, obj, form, change)
    #
    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         if isinstance(instance, ProductAttribute):
    #             old_instance = ProductAttribute.objects.get(id=instance.id)
    #             if old_instance.sale_price != instance.sale_price:
    #                 accountant_invoicer = AccountantInvoicer()
    #                 sendgrid_client = SendGridClient()
    #
    #                 pdf = (
    #                     accountant_invoicer.generate_product_price_change_notification(
    #                         old_instance, instance, request.build_absolute_uri()
    #                     )
    #                 )
    #                 sendgrid_client.send_mail(
    #                     [
    #                         "lilanikolova@yahoo.com",
    #                         "info@trendiko.mk",
    #                         "thefrisb@gmail.com",
    #                     ],
    #                     f"{instance.get_product_title_for_accountant_invoice()} - Промена на цена",
    #                     "<strong>Во attachment</strong>",
    #                     pdf,
    #                 )
    #         instance.save()
    #     formset.save_m2m()


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
            "Styling",
            {
                "classes": ("collapse",),
                "fields": (
                    "background_image",
                    "banner_css",
                    "headline_css",
                    "promotion_text_css",
                    "discount_bar_css",
                    "link_css",
                    "show_logo_icon",
                ),
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


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    search_fields = ["title", "product__title", "stock_item__title"]

    class Meta:
        model = ProductAttribute


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer"]
    list_filter = ["product", "is_default"]
    search_fields = ["question", "answer", "product__title"]
    autocomplete_fields = ["product"]
    form = FrequentlyAskedQuestionAdminForm

    class Meta:
        model = FrequentlyAskedQuestion


@admin.register(ShopClient)
class ShopClient(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "city",
        "total_orders_count",
        "total_revenue",
        "total_profit",
        "dashboard_link",
    ]

    search_fields = ["name", "phone", "city"]
    readonly_fields = ["total_revenue", "total_profit"]

    def total_orders_count(self, obj):
        return obj.orders.count()

    def dashboard_link(self, obj):
        """
        Method that returns a link to the client's dashboard in the admin list view.
        """
        # Construct URL with reverse using the view's name and client's primary key
        url = reverse("shop_manager:client_dashboard", kwargs={"pk": obj.pk})
        # Create an HTML anchor tag
        return format_html(
            '<a href="{}" style="color: #ff9800; background-color: #333; padding: 2px 10px; border-radius: 5px; text-decoration: none;" target="_blank">View Dashboard</a>',
            url,
        )

    dashboard_link.short_description = "Dashboard link"
    dashboard_link.admin_order_field = "name"

    class Meta:
        model = ShopClient


admin.site.register(BrandPage)
