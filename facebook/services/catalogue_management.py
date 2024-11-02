import os
import csv  # Import the csv module

import xlsxwriter
from decouple import config
from django.conf import settings

from shop.models import Product


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
        self.output_file_xlsx = os.path.join(
            settings.MEDIA_ROOT, "facebook_catalogue_feed.xlsx"
        )
        self.output_file_csv = os.path.join(
            settings.MEDIA_ROOT, "facebook_catalogue_feed.csv"
        )  # Define CSV output path

    def make_xlsx_catalogue_feed(self):
        if os.path.exists(self.output_file_xlsx):
            os.remove(self.output_file_xlsx)

        workbook = xlsxwriter.Workbook(self.output_file_xlsx)
        worksheet = workbook.add_worksheet()

        row = 0
        row = self.make_headers(worksheet, row, 0)

        for product in self.products:
            if product.type == Product.ProductType.VARIABLE:
                for attribute in product.attributes.all():
                    self.write_attribute(worksheet, row, product, attribute)
                    row += 1
            else:
                self.write_product(worksheet, row, product)
                row += 1

        workbook.close()
        return self.output_file_xlsx

    def make_csv_catalogue_feed(self):
        if os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)

        headers = [
            "id",
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
        ]

        with open(self.output_file_csv, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # Write the header row

            for product in self.products:
                if product.type == Product.ProductType.VARIABLE:
                    for attribute in product.attributes.all():
                        row = self.get_attribute_row(product, attribute)
                        writer.writerow(row)
                else:
                    row = self.get_product_row(product)
                    writer.writerow(row)

        return self.output_file_csv

    def make_headers(self, worksheet, row, col):
        headers = [
            "id",
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
        ]

        for i, header in enumerate(headers):
            worksheet.write(row, col + i, header)

        row += 1
        return row

    def write_attribute(self, worksheet, row, product, attribute):
        id_key = f"{product.id}-{attribute.id}"
        title = f"{product.title} - {attribute.title}"
        description = self.get_short_description(product)
        availability = self.get_availability(product)
        condition = "new"
        price = f"{attribute.regular_price} {self.currency}"
        link = f"{self.base_url}{product.get_absolute_url()}"
        # Check if attribute has thumbnail
        image_link = self.base_url + attribute.get_thumbnails().get("jpg", "")
        brand = self.brand
        sale_price = f"{attribute.sale_price} {self.currency}"
        additional_image_link = self.get_additional_images(product)
        rich_text_description = product.description

        worksheet.write(row, 0, id_key)
        worksheet.write(row, 1, title)
        worksheet.write(row, 2, description)
        worksheet.write(row, 3, availability)
        worksheet.write(row, 4, condition)
        worksheet.write(row, 5, price)
        worksheet.write(row, 6, link)
        worksheet.write(row, 7, image_link)
        worksheet.write(row, 8, brand)
        worksheet.write(row, 9, sale_price)
        worksheet.write(row, 10, additional_image_link)
        worksheet.write(row, 11, "unisex")
        worksheet.write(row, 12, rich_text_description)

    def get_attribute_row(self, product, attribute):
        id_key = f"{product.id}-{attribute.id}"
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
        ]

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
            return product.short_description
        else:
            return "Нема опис"

    def write_product(self, worksheet, row, product):
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

        worksheet.write(row, 0, id_key)
        worksheet.write(row, 1, title)
        worksheet.write(row, 2, description)
        worksheet.write(row, 3, availability)
        worksheet.write(row, 4, condition)
        worksheet.write(row, 5, price)
        worksheet.write(row, 6, link)
        worksheet.write(row, 7, image_link)
        worksheet.write(row, 8, brand)
        worksheet.write(row, 9, sale_price)
        worksheet.write(row, 10, additional_image_link)
        worksheet.write(row, 11, "unisex")
        worksheet.write(row, 12, rich_text_description)

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
        ]
