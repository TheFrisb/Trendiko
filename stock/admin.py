from django import forms
from django.contrib import admin

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
    list_display = ["title", "sku", "label"]

    form = StockItemForm


@admin.register(ReservedStockItem)
class ReservedStockItemAdmin(admin.ModelAdmin):
    search_fields = ["import_item__stock_item__title", "order_item__stock_item_title"]
