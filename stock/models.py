from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models

from common.models import BaseProduct, TimeStampedModel


# Create your models here.
class StockItem(BaseProduct):
    qr_code = models.ImageField(
        upload_to="stock_items/qr_codes/%Y/%m/%d/", blank=True, verbose_name="QR Code"
    )
    sku = models.CharField(max_length=255, unique=True, verbose_name="SKU")
    label = models.CharField(max_length=255, verbose_name="Label")
    stock = models.PositiveIntegerField(default=0, verbose_name="Залиха")

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

    class Meta:
        verbose_name = "Магацински Продукт"
        verbose_name_plural = "Магацински Продукт"


class Import(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name="Име на увоз")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Увоз"
        verbose_name_plural = "Увози"


class ImportItem(TimeStampedModel):
    parentImport = models.ForeignKey(Import, on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количина")
    price_no_vat = models.PositiveIntegerField(default=0, verbose_name="Цена без ДДВ")
    price_vat = models.PositiveIntegerField(default=0, verbose_name="Цена со ДДВ")
    price_vat_and_customs = models.PositiveIntegerField(
        default=0, verbose_name="Цена со ДДВ и царина"
    )

    def __str__(self):
        return f"{self.stock_item.title} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.stock_item.stock += self.quantity
        self.stock_item.save()
        super().save(*args, **kwargs)

    def vat_price(self):
        return self.price * 0.18

    class Meta:
        verbose_name = "Увозен Продукт"
        verbose_name_plural = "Увозени Продукти"
