from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Product, ProductAttribute, Category, Review, ProductImage


# Register your models here.
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "category": FilteredSelectMultiple("Category", is_stacked=False),
        }


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = ["title", "status", "type", "regular_price", "sale_price"]
    list_filter = ["status", "type"]
    search_fields = ["title"]
    inlines = [ProductImageInline, ProductAttributeInline]

    class Meta:
        model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_filter = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Category


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "name", "rating", "created_at"]
    list_filter = ["product", "name", "rating"]
    search_fields = ["product", "name"]

    class Meta:
        model = Review
