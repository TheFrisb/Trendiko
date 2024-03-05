from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Product, ProductAttribute, Category, Review, ProductImage, BrandPage


# Register your models here.
class ProductAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=FilteredSelectMultiple(verbose_name="Categories", is_stacked=False),
    )

    class Meta:
        model = Product
        fields = "__all__"


class ProductAttributeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        attribute_types = set()
        for form in self.forms:
            if not form.cleaned_data:
                continue  # Skip empty forms
            attribute_type = form.cleaned_data.get("type")
            attribute_types.add(attribute_type)
            if len(attribute_types) > 1:
                raise ValidationError("All attributes must be of the same type.")


class ProductAttributeInline(admin.TabularInline):
    autocomplete_fields = ["stock_item"]
    model = ProductAttribute
    extra = 0
    fields = ["type", "name", "value", "price", "stock_item"]
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
    list_display = ["title", "status", "type", "regular_price", "sale_price"]
    list_filter = ["status", "type"]
    search_fields = ["title"]
    inlines = [ProductImageInline, ProductAttributeInline]
    readonly_fields = ["slug"]

    class Meta:
        model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_filter = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

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


admin.site.register(BrandPage)
