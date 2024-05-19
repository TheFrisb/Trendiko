from io import BytesIO

import qrcode
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.db.models import Sum, IntegerField, F

from common.models import BaseProduct, TimeStampedModel
from shop.models import Product, ProductAttribute


# Create your models here.
class StockItem(BaseProduct):
    qr_code = models.ImageField(
        upload_to="stock_items/qr_codes/%Y/%m/%d/", blank=True, verbose_name="QR Code"
    )
    sku = models.CharField(
        max_length=255, unique=True, verbose_name="SKU", db_index=True
    )
    label = models.CharField(max_length=255, verbose_name="Label")
    stock = models.PositiveIntegerField(
        default=0, verbose_name="Вистинска залиха, без резервирана"
    )

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.sku)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        temp_handle = BytesIO()
        img.save(temp_handle, format="png")
        temp_handle.seek(0)

        file = File(temp_handle, name=f"{self.sku}.png")

        return file

    @property
    @admin.display(description="Вкупна резервирана залиха")
    def reserved_stock(self):
        # for items in import items sum the reserved stock and return
        if self.import_items.exists():
            return sum([item.reserved_stock for item in self.import_items.all()])
        return 0

    @property
    @admin.display(description="Достапна залиха за продажба")
    def available_stock(self):
        return self.stock - self.reserved_stock

    class Meta:
        verbose_name = "Stock Item"
        verbose_name_plural = "Stock Items"

    def __str__(self):
        return f"[{self.sku}] {self.title}, {self.available_stock} items in stock"


class Import(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name="Име на увоз")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    ad_spend = models.IntegerField(default=0, verbose_name="Ad Spend")

    def get_sales_data(self):
        stock_item_ids = self.import_items.values_list(
            "stock_item_id", flat=True
        ).distinct()

        analytics_data = {
            "total_sale_price_for_all_items": 0,
            "total_sale_price_for_all_sold_items": 0,
            "total_sale_price_for_all_available_stock": 0,
            "profit": 0,
        }

        products = (
            Product.objects.filter(
                stock_item__id__in=stock_item_ids, type=Product.ProductType.SIMPLE
            )
            .annotate(
                total_sale_price_for_all_items=Sum(
                    F("sale_price") * F("stock_item__import_items__initial_quantity"),
                    output_field=IntegerField(),
                ),
                total_sale_price_for_all_available_stock=Sum(
                    F("sale_price")
                    * (
                        F("stock_item__import_items__quantity")
                        - F("stock_item__import_items__reserved_stock")
                    ),
                    output_field=IntegerField(),
                ),
            )
            .distinct()
            .values(
                "total_sale_price_for_all_items",
                "total_sale_price_for_all_available_stock",
            )
        )

        attributes = (
            ProductAttribute.objects.filter(product__stock_item__id__in=stock_item_ids)
            .annotate(
                total_sale_price_for_all_items=Sum(
                    F("sale_price") * F("stock_item__import_items__initial_quantity"),
                    output_field=IntegerField(),
                ),
                total_sale_price_for_all_available_stock=Sum(
                    F("sale_price")
                    * (
                        F("stock_item__import_items__quantity")
                        - F("stock_item__import_items__reserved_stock")
                    ),
                    output_field=IntegerField(),
                ),
            )
            .distinct()
            .values(
                "total_sale_price_for_all_items",
                "total_sale_price_for_all_available_stock",
            )
        )

        reserved_stock_items = (
            ReservedStockItem.objects.filter(
                import_item__stock_item__id__in=stock_item_ids
            )
            .annotate(
                total_sale_price_for_all_sold_items=Sum(
                    models.F("order_item__price") * models.F("quantity")
                ),
                total_stock_price_for_all_sold_items=Sum(
                    models.F("import_item__price_vat_and_customs")
                    * models.F("quantity")
                ),
            )
            .values(
                "total_sale_price_for_all_sold_items",
                "total_stock_price_for_all_sold_items",
            )
        )

        total_all_items = sum(
            [
                product["total_sale_price_for_all_items"]
                for product in products
                if product["total_sale_price_for_all_items"]
            ]
        )
        total_all_items += sum(
            [
                attribute["total_sale_price_for_all_items"]
                for attribute in attributes
                if attribute["total_sale_price_for_all_items"]
            ]
        )

        total_all_sold_items = sum(
            [
                reserved_stock_item["total_sale_price_for_all_sold_items"]
                for reserved_stock_item in reserved_stock_items
                if reserved_stock_item["total_sale_price_for_all_sold_items"]
            ]
        )

        total_all_available_stock = sum(
            [
                product["total_sale_price_for_all_available_stock"]
                for product in products
                if product["total_sale_price_for_all_available_stock"]
            ]
        )

        total_all_available_stock += sum(
            [
                attribute["total_sale_price_for_all_available_stock"]
                for attribute in attributes
                if attribute["total_sale_price_for_all_available_stock"]
            ]
        )

        total_all_sold_stock_price = sum(
            [
                reserved_stock_item["total_stock_price_for_all_sold_items"]
                for reserved_stock_item in reserved_stock_items
                if reserved_stock_item["total_stock_price_for_all_sold_items"]
            ]
        )

        analytics_data["total_sale_price_for_all_items"] = total_all_items
        analytics_data["total_sale_price_for_all_sold_items"] = total_all_sold_items
        analytics_data[
            "total_sale_price_for_all_available_stock"
        ] = total_all_available_stock

        analytics_data["profit"] = (
            analytics_data["total_sale_price_for_all_sold_items"]
            - total_all_sold_stock_price
            - (self.ad_spend + (self.ad_spend * 0.1))
            - (analytics_data["total_sale_price_for_all_sold_items"] * 0.1)
        )
        return analytics_data

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Увоз"
        verbose_name_plural = "Увози"


class ImportItem(TimeStampedModel):
    parentImport = models.ForeignKey(
        Import, on_delete=models.CASCADE, related_name="import_items"
    )
    stock_item = models.ForeignKey(
        StockItem, on_delete=models.CASCADE, related_name="import_items"
    )
    initial_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Увезена количина"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Моментална залиха", db_index=True
    )
    price_no_vat = models.PositiveIntegerField(default=0, verbose_name="Цена без ДДВ")
    price_vat = models.PositiveIntegerField(default=0, verbose_name="Цена со ДДВ")
    price_vat_and_customs = models.PositiveIntegerField(
        default=0, verbose_name="Цена со ДДВ и царина"
    )
    reserved_stock = models.PositiveIntegerField(
        default=0, verbose_name="Резервирана залиха"
    )

    def __str__(self):
        return f"[{self.parentImport.title}] {self.stock_item.sku} {self.stock_item.title} - {self.calculate_max_available_reservation()} in stock"

    def save(self, *args, **kwargs):
        self.stock_item.stock = self.calculate_parent_stock()
        self.stock_item.save()
        super().save(*args, **kwargs)

    def calculate_parent_stock(self):
        import_items = ImportItem.objects.filter(stock_item=self.stock_item).exclude(
            pk=self.pk
        )
        stock = sum([import_item.quantity for import_item in import_items])
        return stock + self.quantity

    def vat_price(self):
        return self.price * 0.18

    def calculate_max_available_reservation(self):
        return self.quantity - self.reserved_stock

    class Meta:
        verbose_name = "Увозен Продукт"
        verbose_name_plural = "Увозени Продукти"


class ReservedStockItem(TimeStampedModel):
    class Status(models.TextChoices):
        """Product Status"""

        PENDING = "PENDING", "Pending"
        ARCHIVED = "ARCHIVED", "Archived"
        DEPLETED = "DEPLETED", "Depleted"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    order_item = models.ForeignKey(
        "cart.OrderItem",
        on_delete=models.CASCADE,
        related_name="reserved_stock_items",
    )
    import_item = models.ForeignKey(ImportItem, on_delete=models.PROTECT, null=True)
    initial_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Почетна количина"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количина")

    # def __str__(self):
    #     return (
    #         f"Резервација за {self.order_item.product.title} - {self.initial_quantity}"
    #         f" од {self.import_item.stock_item.title}"
    #     )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.quantity = self.initial_quantity

        self.import_item.reserved_stock = self.calculate_reserved_stock()
        if self.import_item.reserved_stock > self.import_item.quantity:
            raise ValidationError(
                {
                    "error": "The reserved stock cannot be greater than the import item quantity",
                    "order_item": self.order_item,
                }
            )

        self.import_item.save()
        if self.quantity == 0:
            self.status = self.Status.DEPLETED

        super().save(*args, **kwargs)

    def calculate_reserved_stock(self):
        reserved_stocks = ReservedStockItem.objects.filter(
            import_item=self.import_item, status=self.Status.PENDING
        ).exclude(pk=self.pk)
        reserved_stock = sum(
            [reserved_stock.quantity for reserved_stock in reserved_stocks]
        )

        if self.status == self.Status.PENDING:
            reserved_stock += self.quantity

        return reserved_stock
