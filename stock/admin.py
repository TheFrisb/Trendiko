from django.contrib import admin

# Register your models here.
from .models import StockItem, ImportItem, Import


class ImportItemInline(admin.StackedInline):
    model = ImportItem
    extra = 1
    autocomplete_fields = ["stock_item"]


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    inlines = [ImportItemInline]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    search_fields = ["label", "sku"]
