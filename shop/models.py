import random

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from transliterate import translit

from common.models import CATEGORY_THUMBNAIL_DIMENSIONS, IMAGE_QUALITY, IMAGE_DIMENSIONS
from common.models import TimeStampedModel, BaseProduct, SimplePage


# Create your models here.


class Category(TimeStampedModel):
    name = models.CharField(max_length=200, verbose_name="Име")
    # parent = models.ForeignKey(
    #     "self",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name="Припаѓа на",
    #     related_name="subcategories",
    # )
    promotion_text = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Текст за промоција"
    )
    promotion_image = ProcessedImageField(
        upload_to="categories/%Y/%m/%d/",
        processors=[ResizeToFill(*CATEGORY_THUMBNAIL_DIMENSIONS)],
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
        null=True,
        blank=True,
        verbose_name="Слика за промоција (150px X 150px)",
    )
    promotion_image_png = ImageSpecField(
        source="promotion_image",
        format="PNG",
        options={"quality": IMAGE_QUALITY},
    )

    background_image = ProcessedImageField(
        upload_to="categories/%Y/%m/%d/",
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
        null=True,
        blank=True,
        verbose_name="Позадинска слика",
    )
    banner_css = models.TextField(
        null=True, blank=True, verbose_name="Banner CSS (стави !important)"
    )
    headline_css = models.TextField(
        null=True, blank=True, verbose_name="Headline CSS (стави !important)"
    )
    discount_bar_css = models.TextField(
        null=True, blank=True, verbose_name="Discount Bar CSS (стави !important)"
    )
    promotion_text_css = models.TextField(
        null=True, blank=True, verbose_name="Promotion Text CSS (стави !important)"
    )
    link_css = models.TextField(
        null=True, blank=True, verbose_name="Link CSS (стави !important)"
    )
    show_logo_icon = models.BooleanField(
        default=True, verbose_name="Прикажи лого икона (на промотивна категорија)"
    )

    is_on_promotion = models.BooleanField(default=False, verbose_name="Промоција")
    max_discount = models.PositiveIntegerField(verbose_name="Максимален попуст")
    is_default = models.BooleanField(
        default=False, verbose_name="Стандардна категорија"
    )
    slug = models.SlugField(
        blank=True, unique=True, verbose_name="Slug", max_length=300, db_index=True
    )
    display_order = models.IntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, "mk", reversed=True)
            slug_candidate = slugify(latin_name)
            unique_slug = slug_candidate
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = "{}-{}".format(slug_candidate, num)
                num += 1
            self.slug = unique_slug

        if self.is_on_promotion:
            qs = Category.objects.filter(is_on_promotion=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_on_promotion=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category_page", kwargs={"slug": self.slug})

    def __str__(self):
        # if self.parent is not None:
        # return f"[{self.parent}] {self.name}"
        return self.name

    class Meta:
        verbose_name = "Категорија"
        verbose_name_plural = "Категории"
        ordering = ["display_order"]


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
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.PUBLISHED,
        verbose_name="Статус",
        db_index=True,
    )
    type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.SIMPLE,
        verbose_name="Тип",
    )
    slug = models.SlugField(
        blank=True, unique=True, db_index=True, verbose_name="Slug", max_length=300
    )
    categories = models.ManyToManyField(
        Category, related_name="products", verbose_name="Категории", db_index=True
    )
    short_description = models.TextField(
        null=True, blank=True, verbose_name="Краток опис"
    )
    regular_price = models.PositiveIntegerField(verbose_name="Regular price")
    sale_price = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Sale price"
    )
    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Stock Item",
    )
    description = RichTextUploadingField(verbose_name="Опис")
    technical_specifications = RichTextUploadingField(
        null=True, blank=True, verbose_name="Технички спецификации"
    )
    free_shipping = models.BooleanField(
        default=False, verbose_name="Бесплатна испорака", db_index=True
    )

    @property
    def selling_price(self):
        return self.sale_price if self.sale_price else self.regular_price

    def review_data(self):
        reviews = self.reviews.all()
        if reviews:
            rating = sum([review.rating for review in reviews]) / reviews.count()
            closest_half = int(round(rating * 2) / 2)
            return {
                "rating": rating,
                "closest_half": closest_half,
                "count": len(reviews),
            }

    def isVariable(self):
        return self.type == self.ProductType.VARIABLE

    def isOutOfStock(self):
        return self.status == self.ProductStatus.OUT_OF_STOCK

    def get_product_misc_data(self):
        review_data = self.review_data()
        money_saved = self.regular_price - self.selling_price
        money_saved_percent = int((money_saved / self.regular_price) * 100)

        # select all faq items that have is_default set to True or belong to the product
        standard_faq = Q(is_default=True)
        product_faq = Q(product=self)
        faq_items = FrequentlyAskedQuestion.objects.filter(
            standard_faq | product_faq
        ).order_by("-is_default")

        attribute_label = None
        if self.type == self.ProductType.VARIABLE and self.attributes.exists():
            attribute_instance = self.attributes.first()
            attribute_label = attribute_instance.get_attribute_display(
                attribute_instance.type
            )

        return {
            "review_data": review_data,
            "money_saved": money_saved,
            "money_saved_percent": money_saved_percent,
            "faq_items": faq_items,
            "attribute_label": attribute_label,
            "sellable_stock": self.get_sellable_stock_to_show(),
        }

    @property
    def has_free_shipping(self):
        return self.free_shipping or self.selling_price > 1500

    @property
    def get_discount(self):
        if self.sale_price and self.regular_price:
            return int(
                (self.regular_price - self.sale_price) / self.regular_price * 100
            )
        return 0

    @property
    def get_attributes_price_range(self):
        if self.attributes.exists():
            prices = [attribute.sale_price for attribute in self.attributes.all()]
            return {
                "min": min(prices),
                "max": max(prices),
            }
        return {
            "min": self.sale_price,
            "max": self.sale_price,
        }

    def get_sellable_stock_to_show(self):
        if self.stock_item and self.stock_item.stock < 10:
            return self.stock_item.stock
        return random.randint(5, 10)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.title, "mk", reversed=True)
            slug_candidate = slugify(latin_name)
            unique_slug = slug_candidate
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = "{}-{}".format(slug_candidate, num)
                num += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_page", kwargs={"slug": self.slug})

    def get_product_title_for_accountant_invoice(self):
        return self.title

    def get_thumbnail_absolute_url(self):
        return self.thumbnail.url

    @property
    def get_seo_title(self):
        return (
            self.seo_tags.seo_title
            if hasattr(self, "seo_tags") and self.seo_tags.seo_title
            else self.title
        )

    @property
    def get_seo_description(self):
        return (
            self.seo_tags.seo_description
            if hasattr(self, "seo_tags") and self.seo_tags.seo_description
            else self.short_description
        )

    @property
    def get_seo_image(self):
        if (
                hasattr(self, "seo_tags")
                and self.seo_tags.seo_image
                and self.seo_tags.seo_image.name
        ):
            return self.seo_tags.seo_image.url

        if self.thumbnail and self.thumbnail.name:
            return self.thumbnail.url

        return None

    def create_seo_tags(self):
        ProductSeoTags.objects.create(
            product=self,
            seo_title=self.title,
            seo_description=self.short_description,
            seo_image=self.thumbnail,
        )

    class Meta:
        verbose_name = "Производ"
        verbose_name_plural = "Производи"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Производ",
    )
    image = ProcessedImageField(
        upload_to="products/gallery/%Y/%m/%d/",
        processors=[ResizeToFill(*IMAGE_DIMENSIONS)],
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
        verbose_name="Gallery Image",
    )
    image_png = ImageSpecField(
        source="image",
        format="PNG",
        options={"quality": IMAGE_QUALITY},
    )


class ProductAttribute(BaseProduct):
    """Product Attribute Model"""

    class ProductAttributeType(models.TextChoices):
        """Product Attribute Type"""

        COLOR = "color", _("боја")
        SIZE = "size", _("големина")
        OFFER = "offer", _("понуда")
        # PROMOTED = "cart_offer", _("Cart Offer")

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attributes",
        verbose_name="Продукт",
    )
    type = models.CharField(
        max_length=20,
        choices=ProductAttributeType.choices,
        default=ProductAttributeType.COLOR,
        verbose_name="Тип",
    )
    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Stock Item",
    )
    value = models.CharField(max_length=140, verbose_name="Содржина")
    regular_price = models.PositiveIntegerField(verbose_name="Цена без попуст")
    sale_price = models.PositiveIntegerField(verbose_name="Цена")

    def get_attribute_display(self, attribute_type_value):
        return self.ProductAttributeType(attribute_type_value).label

    def get_thumbnail_loops(self):
        if self.thumbnail and self.thumbnail.name:
            return {
                "webp": self.thumbnail_loop.url,
                "jpg": self.thumbnail_loop_as_jpeg.url,
            }
        return {
            "webp": self.product.thumbnail_loop.url,
            "jpg": self.product.thumbnail_loop_as_jpeg.url,
        }

    def get_thumbnails(self):
        if self.thumbnail and self.thumbnail.name:
            return {
                "webp": self.thumbnail.url,
                "jpg": self.thumbnail_as_jpeg.url,
            }
        return {
            "webp": self.product.thumbnail.url,
            "jpg": self.product.thumbnail_as_jpeg.url,
        }

    @property
    def money_saved(self):
        if self.sale_price and self.regular_price:
            return self.regular_price - self.sale_price
        return 0

    @property
    def money_saved_percent(self):
        if self.sale_price and self.regular_price:
            return int(
                (self.regular_price - self.sale_price) / self.regular_price * 100
            )
        return 0

    def get_product_title_for_accountant_invoice(self):
        return f"{self.product.get_product_title_for_accountant_invoice()} - {self.title} {self.get_attribute_display(self.type)}"

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

    def __str__(self):
        return self.get_product_title_for_accountant_invoice()


class Review(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    # int field 1 to 5
    rating = models.PositiveIntegerField()
    name = models.CharField(max_length=140)
    content = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to="products/%Y/%m/%d/",
        processors=[ResizeToFit(width=400, upscale=False)],
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
        null=True,
        blank=True,
    )
    image_png = ImageSpecField(
        source="image",
        format="PNG",
        options={"quality": IMAGE_QUALITY},
    )

    def __str__(self):
        return f"{self.product.title} - {self.rating}"

    class Meta:
        verbose_name = "Рецензија"
        verbose_name_plural = "Рецензии"


class FrequentlyAskedQuestion(TimeStampedModel):
    question = models.CharField(max_length=200, verbose_name="Прашање")
    answer = models.TextField(verbose_name="Одговор")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="faqItems",
        verbose_name="Производ",
        db_index=True,
        null=True,
        blank=True,
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="Стандардно прашање (Вклучено за секој производ)",
        db_index=True,
    )

    class Meta:
        verbose_name = "Често поставени прашања"
        verbose_name_plural = "Често поставени прашања"


class BrandPage(SimplePage):
    def get_absolute_url(self):
        return reverse("shop:brand_page", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Информативна страница"
        verbose_name_plural = "Информативни страници"


class ShopClient(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name="Име на фирма/клиент")
    phone = models.CharField(
        max_length=255, verbose_name="Телефонски број", blank=True, null=True
    )
    city = models.CharField(max_length=255, verbose_name="Град", blank=True, null=True)
    total_revenue = models.IntegerField(default=0)
    total_profit = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенти"
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.name}"


class CartOffers(TimeStampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_offers"
    )
    sale_price = models.PositiveIntegerField(verbose_name="Понудена цена")
    sale_text = models.CharField(max_length=200, verbose_name="Текст за понуда")
    display_order = models.IntegerField(default=0, db_index=True)

    @property
    def thumbnails(self):
        return {
            "webp": self.product.thumbnail_loop.url,
            "jpg": self.product.thumbnail_loop_as_jpeg.url,
        }

    class Meta:
        verbose_name = "Понуда за кошничка"
        verbose_name_plural = "Понуди за кошничка"
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.title} - {self.sale_price}"


class ProductSeoTags(TimeStampedModel):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="seo_tags"
    )
    seo_title = models.CharField(max_length=200, verbose_name="SEO Title")
    seo_description = models.TextField(verbose_name="SEO Description")
    seo_image = ProcessedImageField(
        upload_to="products/%Y/%m/%d/",
        format="PNG",
        options={"quality": IMAGE_QUALITY},
        null=True,
        blank=True,
        verbose_name="SEO Image",
    )
