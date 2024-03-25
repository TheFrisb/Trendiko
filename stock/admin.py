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
            if quantity < instance.reserved_stock:
                raise forms.ValidationError(
                    "Quantity cannot be less than the reserved stock."
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
    readonly_fields = ["reserved_stock"]

    form = ImportItemForm


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    inlines = [ImportItemInline]


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    search_fields = ["label", "sku"]
    readonly_fields = ["stock", "available_stock", "reserved_stock", "qr_code"]

    form = StockItemForm


@admin.register(ReservedStockItem)
class ReservedStockItemAdmin(admin.ModelAdmin):
    pass
