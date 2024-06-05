from django import forms
from django.contrib import admin
from django.db.models import Subquery, OuterRef, DecimalField, Sum

from shop.models import Product, ProductAttribute
# Register your models here.
from .models import StockItem, ImportItem, Import, ReservedStockItem


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = "__all__"

    def clean_sku(self):
        sku = self.cleaned_data["sku"]
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            if instance.sku != sku:
                raise forms.ValidationError(
                    "Changing the SKU of an existing StockItem is not allowed."
                )
        return sku


class ImportItemForm(forms.ModelForm):
    def clean_quantity(self):
        instance = getattr(self, "instance", None)
        quantity = self.cleaned_data["quantity"]

        if instance and instance.pk:
            if quantity > instance.initial_quantity:
                raise forms.ValidationError(
                    "Quantity cannot be greater than the initial quantity."
                )

        return quantity

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.quantity = instance.initial_quantity

        if commit:
            instance.save()
        return instance


class ImportItemInline(admin.StackedInline):
    model = ImportItem
    extra = 1
    autocomplete_fields = ["stock_item"]
    form = ImportItemForm


@admin.register(ImportItem)
class ImportItemAdmin(admin.ModelAdmin):
    search_fields = ["stock_item__title"]


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    inlines = [ImportItemInline]
    readonly_fields = ["ad_spend"]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    search_fields = ["label", "sku", "title"]
    readonly_fields = ["stock", "qr_code"]
    list_display = [
        "title",
        "sku",
        "label",
        "stock_price",
        "sale_price",
        "stock",
        "imported_stock",
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        latest_import_price = (
            ImportItem.objects.filter(stock_item=OuterRef("pk"))
            .order_by("-created_at")
            .values("price_vat_and_customs")[:1]
        )

        queryset = queryset.annotate(
            annotated_stock_price=Subquery(
                latest_import_price, output_field=DecimalField()
            )
        )

        product_sale_price = Product.objects.filter(stock_item=OuterRef("pk")).values(
            "sale_price"
        )[:1]

        product_attribute_sale_price = ProductAttribute.objects.filter(
            stock_item=OuterRef("pk")
        ).values("sale_price")[:1]

        queryset = (
            queryset.annotate(
                annotated_sale_price=Subquery(
                    product_sale_price, output_field=DecimalField()
                )
            )
            .annotate(
                annotated_attribute_sale_price=Subquery(
                    product_attribute_sale_price, output_field=DecimalField()
                )
            )
            .annotate(total_imported_stock=Sum("import_items__initial_quantity"))
        )

        return queryset

    def stock_price(self, obj):
        return obj.annotated_stock_price

    stock_price.short_description = "Набавна цена"
    stock_price.admin_order_field = "annotated_stock_price"

    def sale_price(self, obj):
        return (
            obj.annotated_sale_price
            if obj.annotated_sale_price is not None
            else obj.annotated_attribute_sale_price
        )

    sale_price.short_description = "Продажна цена"
    sale_price.admin_order_field = "annotated_sale_price"

    def imported_stock(self, obj):
        return obj.total_imported_stock

    imported_stock.short_description = "Увезена залиха"
    imported_stock.admin_order_field = "total_imported_stock"

    form = StockItemForm


@admin.register(ReservedStockItem)
class ReservedStockItemAdmin(admin.ModelAdmin):
    search_fields = ["import_item__stock_item__title", "order_item__stock_item_title"]
