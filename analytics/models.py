from django.db import models

from common.models import TimeStampedModel
from transliterate import translit
from django.utils.text import slugify


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

    class Meta:
        verbose_name = "Campaign Summary"
        verbose_name_plural = "Campaign Summaries"


class CampaignEntry(TimeStampedModel):
    campaign = models.ForeignKey(CampaignSummary, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField(
        verbose_name="Quantity of OrderItems Ordered"
    )
    total_sales_price = models.PositiveIntegerField(
        verbose_name="Total Sale Price of all OrderItems"
    )
    total_cost_price = models.PositiveIntegerField(
        verbose_name="Total Cost Price of all OrderItems"
    )
    total_profit = models.PositiveIntegerField(
        verbose_name="Total Profit of all OrderItems"
    )
    total_neto = models.PositiveIntegerField(
        verbose_name="Total Neto of all OrderItems"
    )
    advertisement_cost = models.PositiveIntegerField(
        verbose_name="Total Advertisement Cost"
    )
    product_sale_price = models.PositiveIntegerField(verbose_name="Product Sale Price")
    product_cost_price = models.PositiveIntegerField(verbose_name="Product Cost Price")
    product_profit = models.PositiveIntegerField(verbose_name="Product Profit")
    product_neto = models.PositiveIntegerField(verbose_name="Product Neto")

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
    def __str__(self):
        return f"CampaignEntry for {self.campaign.name} - {self.created_at}"
