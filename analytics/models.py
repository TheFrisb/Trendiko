import datetime

from decouple import config, Csv
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from weasyprint import HTML

from common.mailer.SendGridClient import SendGridClient
from common.models import TimeStampedModel, StoredCounter
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

    def populate_entry(
        self,
        order_items: models.QuerySet,
        ad_spend_data: dict,
        for_date: datetime.datetime,
    ):
        entry = CampaignEntry(parent=self, for_date=for_date)
        entry.populate_data(order_items, ad_spend_data["spend_mkd"])
        return entry

    def get_absolute_url(self):
        return reverse(
            "shop_manager:facebook_campaign_detail_view", kwargs={"slug": self.slug}
        )

    class Meta:
        verbose_name = "Campaign Summary"
        verbose_name_plural = "Campaign Summaries"


class CampaignEntry(TimeStampedModel):
    parent = models.ForeignKey(
        CampaignSummary, on_delete=models.CASCADE, related_name="entries"
    )
    quantity_ordered = models.IntegerField(
        verbose_name="Quantity of OrderItems Ordered", default=0
    )
    total_sales_price = models.IntegerField(
        verbose_name="Total Sale Price of all OrderItems", default=0
    )
    total_cost_price = models.IntegerField(
        verbose_name="Total Cost Price of all OrderItems", default=0
    )
    advertisement_cost = models.FloatField(
        verbose_name="Total Advertisement Cost",
        default=0,
    )
    product_sale_price = models.IntegerField(
        verbose_name="Product Sale Price", default=0
    )
    product_cost_price = models.IntegerField(
        verbose_name="Product Cost Price", default=0
    )
    product_stock_left = models.IntegerField(
        verbose_name="Product Stock Left After Campaign", default=0
    )
    for_date = models.DateTimeField(
        verbose_name="Date for which the data is collected", db_index=True
    )

    import_item_data = models.JSONField()

    @property
    def total_profit(self):
        return self.total_sales_price - self.total_cost_price

    @property
    def product_profit(self):
        return self.product_sale_price - self.product_cost_price

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
        return self.product_sale_price / self.product_profit

    @property
    def total_neto_profit(self):
        return self.total_profit - self.advertisement_cost

    def __str__(self):
        return f"CampaignEntry for {self.parent.name} - {self.created_at}"

    def populate_data(self, order_items: models.QuerySet, ad_spend_data: float):
        import_item_data = {}
        self.populate_static_data(ad_spend_data)
        self.populate_dynamic_data(order_items)

        # save the entry
        self.save()

    def populate_static_data(self, ad_spend_data: float) -> None:
        if self.parent.product.stock_item:
            self.product_stock_left = self.parent.product.stock_item.stock
        else:
            self.product_stock_left = sum(
                attribute.stock_item.stock
                for attribute in self.parent.product.attributes.all().distinct(
                    "stock_item"
                )
            )
        self.product_sale_price = self.parent.product.sale_price
        self.product_cost_price = self.calculate_product_cost_price()
        self.advertisement_cost = ad_spend_data

    def calculate_product_cost_price(self) -> int:
        # Refaktoriri ka ke se trgne rezervirana zaliha
        import_items = ImportItem.objects.filter(
            stock_item=self.parent.product.stock_item
        ).order_by("created_at")

        if not import_items.exists():
            stock_item = self.parent.product.attributes.first().stock_item
            import_items = ImportItem.objects.filter(stock_item=stock_item).order_by(
                "created_at"
            )

        cost_prices = []
        for import_item in import_items:
            if import_item.calculate_max_available_reservation() > 0:
                return import_item.price_vat_and_customs

            cost_prices.append(import_item.price_vat_and_customs)

        return cost_prices[0]

    def populate_dynamic_data(self, order_items: models.QuerySet) -> None:
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


class PriceChange(TimeStampedModel):
    product = models.ForeignKey(
        "shop.Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    attribute = models.ForeignKey(
        "shop.ProductAttribute", on_delete=models.SET_NULL, null=True, blank=True
    )
    product_name = models.TextField()
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    old_stock = models.IntegerField()
    new_stock = models.IntegerField()
    for_date = models.DateTimeField()
    counter = models.IntegerField(default=-1)

    def send_mail(self, mail_to: list[str] = None):
        if not self.product and not self.attribute:
            raise ValueError("Product or Attribute must be set")

        sendgrid_client = SendGridClient()

        pdf = self.generate_pdf()

        if not mail_to:
            mail_to = self.get_mail_recipients()

        sendgrid_client.send_mail(
            mail_to,
            f"{self.get_product_title_for_accountant_invoice()} - Промена на цена",
            "<strong>Во attachment</strong>",
            pdf,
        )

    def get_stock_item(self):
        if self.product:
            return self.product.stock_item
        return self.attribute.stock_item

    def generate_pdf(self):
        if self.counter == -1:
            stored_counter = StoredCounter.objects.get(
                type=StoredCounter.CounterType.PRODUCT_PRICE_CHANGE
            )
            self.counter = stored_counter.get_counter()
            stored_counter.increment_counter()

        old_stock = self.old_stock
        old_total = self.old_price * old_stock
        new_stock = self.new_stock
        new_total = self.new_price * new_stock

        context = {
            "old_price": self.old_price,
            "old_stock": old_stock,
            "old_total": old_total,
            "new_price": self.new_price,
            "new_stock": new_stock,
            "new_total": new_total,
            "price_difference": abs(old_total - new_total),
            "product_title": self.get_product_title_for_accountant_invoice(),
            "counter": self.get_formatted_counter(),
            "current_date": self.for_date.strftime("%d.%m.%Y"),
        }

        html_string = render_to_string("shop_manager/accountant_pdf.html", context)
        return HTML(string=html_string, base_url=settings.WEBSITE_BASE_URL).write_pdf()

    def get_formatted_counter(self):
        date = self.for_date.strftime("%y")
        return f"{self.counter}/{date}"

    def get_product_title_for_accountant_invoice(self):
        if self.product:
            return self.product.get_product_title_for_accountant_invoice()

        return self.attribute.get_product_title_for_accountant_invoice()

    def get_mail_recipients(self):
        return config("ACCOUNTANT_EMAIL_RECIPIENTS", cast=Csv())

    def __str__(self):
        return f"{self.product_name} - {self.for_date}"
