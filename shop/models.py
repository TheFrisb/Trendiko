from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel, BaseProduct


# Create your models here.


class Product(BaseProduct):
    """Product Model"""

    class ProductStatus(models.TextChoices):
        """Product Status"""

        PUBLISHED = "published", _("Published")
        OUT_OF_STOCK = "out_of_stock", _("Out of Stock")
        ARCHIVED = "archived", _("Archived")

    class ProductType(models.TextChoices):
        """Product Type"""

        SIMPLE = "simple", _("Simple")
        VARIABLE = "variable", _("Variable")

    status = models.CharField(
        max_length=20, choices=ProductStatus.choices, default=ProductStatus.PUBLISHED
    )
    type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.SIMPLE
    )

    regular_price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField(null=True, blank=True)
    stock_item = models.ForeignKey(
        "stock.StockItem", on_delete=models.CASCADE, null=True
    )

    @property
    def selling_price(self):
        return self.sale_price if self.sale_price else self.regular_price


class ProductAttribute(TimeStampedModel):
    """Product Attribute Model"""

    class ProductAttributeType(models.TextChoices):
        """Product Attribute Type"""

        COLOR = "color", _("Color")
        SIZE = "size", _("Size")
        OFFER = "offer", _("Offer")
        PROMOTED = "cart_offer", _("Cart Offer")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    type = models.CharField(
        max_length=20,
        choices=ProductAttributeType.choices,
        default=ProductAttributeType.COLOR,
    )
    name = models.CharField(max_length=140)
    content = models.CharField(max_length=140)
    price = models.PositiveIntegerField(null=True, blank=True)
