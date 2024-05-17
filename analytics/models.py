from django.db import models
from django.utils.text import slugify
from transliterate import translit

from common.models import TimeStampedModel
from stock.models import ImportItem


# Create your models here.
class CampaignSummary(TimeStampedModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey("shop.Product", on_delete=models.SET_NULL, null=True)
    campaign_id = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    # create slug on save
    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, "mk", reversed=True)
            self.slug = slugify(latin_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.campaign_id}"

    def populate_entry(self, order_items):
        entry = CampaignEntry(parent=self)
        entry.populate_data(order_items)
        return entry

    class Meta:
        verbose_name = "Campaign Summary"
        verbose_name_plural = "Campaign Summaries"


class CampaignEntry(TimeStampedModel):
    parent = models.ForeignKey(CampaignSummary, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField(
        verbose_name="Quantity of OrderItems Ordered", default=0
    )
    total_sales_price = models.IntegerField(
        verbose_name="Total Sale Price of all OrderItems", default=0
    )
    total_cost_price = models.IntegerField(
        verbose_name="Total Cost Price of all OrderItems", default=0
    )
    total_profit = models.IntegerField(
        verbose_name="Total Profit of all OrderItems", default=0
    )
    advertisement_cost = models.IntegerField(
        verbose_name="Total Advertisement Cost", default=0
    )
    product_sale_price = models.IntegerField(
        verbose_name="Product Sale Price", default=0
    )
    product_cost_price = models.IntegerField(
        verbose_name="Product Cost Price", default=0
    )
    product_profit = models.IntegerField(verbose_name="Product Profit", default=0)
    product_stock_left = models.IntegerField(
        verbose_name="Product Stock Left After Campaign", default=0
    )

    import_item_data = models.JSONField()

    @property
    def cost_per_purchase(self):
        # CPA
        if self.quantity_ordered > 0:
            return self.advertisement_cost / self.quantity_ordered
        return 0

    @property
    def return_on_ad_spend(self):
        # ROAS
        if self.advertisement_cost > 0:
            return self.total_sales_price / self.advertisement_cost
        return self.total_sales_price

    @property
    def return_on_investment(self):
        # ROI
        if self.advertisement_cost > 0:
            return self.total_profit / self.advertisement_cost
        return self.total_profit

    @property
    def break_even_return_on_ad_spend(self):
        # BE-ROAS
        return self.product_sale_price / self.product_neto

    @property
    def total_tax(self):
        return (self.product_sale_price * self.product_cost_price) - (
            (self.product_sale_price * self.quantity_ordered) / 1.18
        )

    @property
    def total_tax_neto(self):
        return (self.product_cost_price * self.quantity_ordered) / 1.18

    @property
    def tax_to_pay(self):
        return self.total_tax - self.total_tax_neto

    def __str__(self):
        return f"CampaignEntry for {self.parent.name} - {self.created_at}"

    def populate_data(self, order_items):
        import_item_data = {}
        self.populate_static_data()
        self.populate_dynamic_data(order_items)

        # save the entry
        self.save()

    def populate_static_data(self):
        self.product_stock_left = self.parent.product.stock_item.available_stock
        self.product_sale_price = self.parent.product.sale_price
        self.product_cost_price = self.calculate_product_cost_price()
        self.product_profit = self.product_sale_price - self.product_cost_price

    def calculate_product_cost_price(self):
        # Refaktoriri ka ke se trgne rezervirana zaliha
        import_items = ImportItem.objects.filter(
            stock_item=self.parent.product.stock_item
        ).order_by("created_at")
        cost_prices = []
        for import_item in import_items:
            if import_item.calculate_max_available_reservation() > 0:
                return import_item.price_vat_and_customs

            cost_prices.append(import_item.price_vat_and_customs)

        return cost_prices[0]

    def populate_dynamic_data(self, order_items):
        import_item_data = {}
        for order_item in order_items:
            self.quantity_ordered += order_item.quantity
            self.total_sales_price += order_item.total_price

            for reserved_item in order_item.reserved_stock_items.all():
                reserved_import_item = reserved_item.import_item

                self.total_cost_price += (
                    reserved_import_item.price_vat_and_customs
                    * reserved_item.initial_quantity
                )

                self.total_profit += (
                    reserved_item.initial_quantity * order_item.price
                ) - self.total_cost_price

                if reserved_import_item.id in import_item_data:
                    import_item_data[reserved_import_item.id][
                        "quantity"
                    ] += reserved_item.initial_quantity
                else:
                    import_item_data[reserved_import_item.id] = {
                        "quantity": reserved_item.initial_quantity,
                        "stock_price": reserved_import_item.price_vat_and_customs,
                    }

        self.import_item_data = import_item_data