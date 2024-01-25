from django.contrib import admin

from .models import Product, ProductAttribute, Category


# Register your models here.
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "type", "regular_price", "sale_price"]
    list_filter = ["status", "type"]
    search_fields = ["title"]
    inlines = [ProductAttributeInline]

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
