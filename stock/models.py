from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models

from common.models import BaseProduct, TimeStampedModel


# Create your models here.
class StockItem(BaseProduct):
    qr_code = models.ImageField(upload_to="stock_items/qr_codes/%Y/%m/%d/", blank=True)
    sku = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)

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
        qr.add_data(self.id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        temp_handle = BytesIO()
        img.save(temp_handle, format="png")
        temp_handle.seek(0)

        file = File(temp_handle, name=f"{self.sku}.png")

        return file


class Import(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ImportItem(TimeStampedModel):
    parentImport = models.ForeignKey(Import, on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.stock_item.title} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.stock_item.stock += self.quantity
        self.stock_item.save()
        super().save(*args, **kwargs)

    def vat_price(self):
        return self.price * 0.18
