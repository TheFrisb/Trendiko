import csv  # Import the csv module
import os

from decouple import config
from django.conf import settings
from django.utils.html import strip_tags

from shop.models import Product, ProductAttribute


class CatalogueManager:
    """
    Facebook feed generator
    """

    def __init__(self):
        self.products = Product.objects.all()
        self.currency = "MKD"
        self.brand = "Trendiko"
        self.base_url = config("BASE_URL")
        self.delimiter = ","

        self.output_file_csv = os.path.join(
            settings.MEDIA_ROOT, "facebook_catalogue_feed.csv"
        )  # Define CSV output path

    def make_csv_catalogue_feed(self):
        if os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)

        headers = [
            "id",
            "item_group_id",
            "title",
            "description",
            "availability",
            "condition",
            "price",
            "link",
            "image_link",
            "brand",
            "sale_price",
            "additional_image_link",
            "gender",
            "rich_text_description",
            "size",
            "color",
            "additional_variant_attribute",
        ]

        with open(
                self.output_file_csv, mode="w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # Write the header row

            for product in self.products:
                if product.type == Product.ProductType.VARIABLE:
                    row = self.get_attribute_product_row(product)
                    writer.writerow(row)
                    for attribute in product.attributes.all():
                        row = self.get_attribute_row(product, attribute)
                        writer.writerow(row)
                else:
                    row = self.get_product_row(product)
                    writer.writerow(row)

        return self.output_file_csv

    def get_product_row(self, product):
        id_key = product.id
        title = product.title
        description = self.get_short_description(product)
        availability = self.get_availability(product)
        condition = "new"
        price = f"{product.regular_price} {self.currency}"
        link = f"{self.base_url}{product.get_absolute_url()}"
        image_link = self.base_url + product.thumbnail_as_jpeg.url
        brand = self.brand
        sale_price = f"{product.sale_price} {self.currency}"
        additional_image_link = self.get_additional_images(product)
        rich_text_description = product.description

        return [
            id_key,
            title,
            description,
            availability,
            condition,
            price,
            link,
            image_link,
            brand,
            sale_price,
            additional_image_link,
            "unisex",
            rich_text_description,
            "",
            "",
            "",
        ]

    def get_attribute_product_row(self, product):
        id_key = ""
        item_group_id = product.id
        title = product.title
        description = self.get_short_description(product)
        availability = ""
        condition = "new"
        price = ""
        link = f"{self.base_url}{product.get_absolute_url()}"
        image_link = self.base_url + product.thumbnail_as_jpeg.url
        brand = self.brand
        sale_price = ""
        additional_image_link = self.get_additional_images(product)
        rich_text_description = product.description

        return [
            id_key,
            item_group_id,
            title,
            description,
            availability,
            condition,
            price,
            link,
            image_link,
            brand,
            sale_price,
            additional_image_link,
            "unisex",
            rich_text_description,
            "",
            "",
            "",
        ]

    def get_attribute_row(self, product, attribute):
        id_key = f"{product.id}-{attribute.id}"
        item_group_id = product.id
        title = f"{product.title} - {attribute.title}"
        description = self.get_short_description(product)
        availability = self.get_availability(product)
        condition = "new"
        price = f"{attribute.regular_price} {self.currency}"
        link = f"{self.base_url}{product.get_absolute_url()}"
        image_link = self.base_url + attribute.get_thumbnails().get("jpg", "")
        brand = self.brand
        sale_price = f"{attribute.sale_price} {self.currency}"
        additional_image_link = self.get_additional_images(product)
        rich_text_description = product.description

        return [
            id_key,
            item_group_id,
            title,
            description,
            availability,
            condition,
            price,
            link,
            image_link,
            brand,
            sale_price,
            additional_image_link,
            "unisex",
            rich_text_description,
            self.write_size_if_needed(attribute),
            self.write_color_if_needed(attribute),
            self.write_offer_if_needed(attribute),
        ]

    def write_size_if_needed(self, attribute: ProductAttribute):
        if attribute.type == ProductAttribute.ProductAttributeType.SIZE:
            return attribute.value
        else:
            return ""

    def write_offer_if_needed(self, attribute: ProductAttribute):
        if attribute.type == ProductAttribute.ProductAttributeType.COLOR:
            return attribute.value
        else:
            return ""

    def write_color_if_needed(self, attribute: ProductAttribute):
        if attribute.type == ProductAttribute.ProductAttributeType.COLOR:
            return attribute.value
        else:
            return ""

    def get_additional_images(self, product):
        string = f"{self.base_url}{product.thumbnail_as_jpeg.url}{self.delimiter}"
        for image in product.images.all():
            string += f"{self.base_url}{image.image_png.url}{self.delimiter}"

        return string[:-1]

    def get_availability(self, product):
        if product.status in [
            Product.ProductStatus.ARCHIVED,
            Product.ProductStatus.OUT_OF_STOCK,
        ]:
            return "out of stock"
        else:
            return "in stock"

    def get_short_description(self, product):
        if product.short_description:
            return strip_tags(product.short_description)
        else:
            return "Нема опис"
