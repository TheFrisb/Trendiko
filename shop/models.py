from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from transliterate import translit

from common.models import CATEGORY_THUMBNAIL_DIMENSIONS, IMAGE_QUALITY, IMAGE_DIMENSIONS
from common.models import TimeStampedModel, BaseProduct, SimplePage


# Create your models here.


class Category(models.Model):
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
        upload_to="products/%Y/%m/%d/",
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

    is_on_promotion = models.BooleanField(default=False, verbose_name="Промоција")
    max_discount = models.PositiveIntegerField(verbose_name="Максимален попуст")
    slug = models.SlugField(
        blank=True, unique=True, verbose_name="Slug", max_length=300, db_index=True
    )

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
    regular_price = models.PositiveIntegerField(verbose_name="Regular price")
    sale_price = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Sale price"
    )
    stock_item = models.ForeignKey(
        "stock.StockItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Магацински предмет",
    )
    description = RichTextUploadingField(verbose_name="Опис")
    has_free_shipping = models.BooleanField(
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

    def get_product_misc_data(self):
        review_data = self.review_data()
        money_saved = self.regular_price - self.selling_price
        money_saved_percent = int((money_saved / self.regular_price) * 100)

        return {
            "review_data": review_data,
            "money_saved": money_saved,
            "money_saved_percent": money_saved_percent,
        }

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


class ProductAttribute(TimeStampedModel):
    """Product Attribute Model"""

    class ProductAttributeType(models.TextChoices):
        """Product Attribute Type"""

        COLOR = "color", _("Color")
        SIZE = "size", _("Size")
        OFFER = "offer", _("Offer")
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
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Магацински предмет",
    )
    name = models.CharField(max_length=140, verbose_name="Име")
    value = models.CharField(max_length=140, verbose_name="Содржина")
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Цена")

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"


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


class BrandPage(SimplePage):
    class Meta:
        verbose_name = "Информативна страница"
        verbose_name_plural = "Информативни страници"
