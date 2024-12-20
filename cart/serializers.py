from rest_framework import serializers

from shop.models import Product
from .models import (
    CartItem,
    ShippingDetails,
    Cart,
    Order,
    OrderItem,
    AbandonedCartDetails,
)


# SUPPORTED_CITIES = [
#     {"latin": "Aerodrom", "cyrillic": "Аеродром"},
#     {"latin": "Aracinovo", "cyrillic": "Арачиново"},
#     {"latin": "Berovo", "cyrillic": "Берово"},
#     {"latin": "Bitola", "cyrillic": "Битола"},
#     {"latin": "Bogdanci", "cyrillic": "Богданци"},
#     {"latin": "Butel", "cyrillic": "Бутел"},
#     {"latin": "Valandovo", "cyrillic": "Валандово"},
#     {"latin": "Veles", "cyrillic": "Велес"},
#     {"latin": "Vinica", "cyrillic": "Виница"},
#     {"latin": "Gazi Baba", "cyrillic": "Гази Баба"},
#     {"latin": "Gevgelija", "cyrillic": "Гевгелија"},
#     {"latin": "Gostivar", "cyrillic": "Гостивар"},
#     {"latin": "Debar", "cyrillic": "Дебар"},
#     {"latin": "Delcevo", "cyrillic": "Делчево"},
#     {"latin": "Demir Kapija", "cyrillic": "Демир Капија"},
#     {"latin": "Demir Hisar", "cyrillic": "Демир Хисар"},
#     {"latin": "Dojran", "cyrillic": "Дојран"},
#     {"latin": "Gjorce Petrov", "cyrillic": "Ѓорче Петров"},
#     {"latin": "Zelenikovo", "cyrillic": "Зелениково"},
#     {"latin": "Ilinden", "cyrillic": "Илинден"},
#     {"latin": "Kavadarci", "cyrillic": "Кавадарци"},
#     {"latin": "Karpos", "cyrillic": "Карпош"},
#     {"latin": "Kisela Voda", "cyrillic": "Кисела Вода"},
#     {"latin": "Kichevo", "cyrillic": "Кичево"},
#     {"latin": "Kocani", "cyrillic": "Кочани"},
#     {"latin": "Kratovo", "cyrillic": "Кратово"},
#     {"latin": "Kriva Palanka", "cyrillic": "Крива Паланка"},
#     {"latin": "Krusevo", "cyrillic": "Крушево"},
#     {"latin": "Kumanovo", "cyrillic": "Куманово"},
#     {"latin": "Mavrovo", "cyrillic": "Маврово"},
#     {"latin": "Makedonska Kamenica", "cyrillic": "Македонска Каменица"},
#     {"latin": "Makedonski Brod", "cyrillic": "Македонски Брод"},
#     {"latin": "Negotino", "cyrillic": "Неготино"},
#     {"latin": "Ohrid", "cyrillic": "Охрид"},
#     {"latin": "Petrovec", "cyrillic": "Петровец"},
#     {"latin": "Pehcevo", "cyrillic": "Пехчево"},
#     {"latin": "Prilep", "cyrillic": "Прилеп"},
#     {"latin": "Probistip", "cyrillic": "Пробиштип"},
#     {"latin": "Radovis", "cyrillic": "Радовиш"},
#     {"latin": "Resen", "cyrillic": "Ресен"},
#     {"latin": "Saraj", "cyrillic": "Сарај"},
#     {"latin": "Sveti Nikole", "cyrillic": "Свети Николе"},
#     {"latin": "Skopje", "cyrillic": "Скопје"},
#     {"latin": "Sopiste", "cyrillic": "Сопиште"},
#     {"latin": "Struga", "cyrillic": "Струга"},
#     {"latin": "Strumica", "cyrillic": "Струмица"},
#     {"latin": "Studenicani", "cyrillic": "Студеничани"},
#     {"latin": "Tetovo", "cyrillic": "Тетово"},
#     {"latin": "Centar", "cyrillic": "Центар"},
#     {"latin": "Cair", "cyrillic": "Чаир"},
#     {"latin": "Cucer Sandevo", "cyrillic": "Чучер-Сандево"},
#     {"latin": "Stip", "cyrillic": "Штип"},
#     {"latin": "Suto Orizari", "cyrillic": "Шуто Оризари"},
# ]
#
# SUPPORTED_MUNICIPALITIES = [
#     {"latin": "Aerodrom", "cyrillic": "Аеродром"},
#     {"latin": "Butel", "cyrillic": "Бутел"},
#     {"latin": "Gazi Baba", "cyrillic": "Гази Баба"},
#     {"latin": "Gjorce Petrov", "cyrillic": "Ѓорче Петров"},
#     {"latin": "Kisela Voda", "cyrillic": "Кисела Вода"},
#     {"latin": "Karpos", "cyrillic": "Карпош"},
#     {"latin": "Centar", "cyrillic": "Центар"},
#     {"latin": "Cair", "cyrillic": "Чаир"},
#     {"latin": "Suto Orizari", "cyrillic": "Шуто Оризари"},
#     {"latin": "Saraj", "cyrillic": "Сарај"},
# ]


class AddProductToCartSerializer(serializers.Serializer):
    """
    Serializer for adding a product to the cart
    """

    product_id = serializers.IntegerField(min_value=1, required=True)
    product_type = serializers.ChoiceField(Product.ProductType.choices, required=True)
    quantity = serializers.IntegerField(min_value=1, max_value=100, required=True)

    attribute_id = serializers.IntegerField(
        min_value=1, required=False, allow_null=True
    )


class AddCartOfferToCartSerializer(serializers.Serializer):
    cart_offer_id = serializers.IntegerField(min_value=1, required=True)


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer for updating a cart item
    """

    quantity = serializers.IntegerField(min_value=1, max_value=100, required=True)


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model
    Used for returning the cart items to the frontend
    """

    has_free_shipping = serializers.SerializerMethodField()
    attribute_title = serializers.SerializerMethodField()
    cart_offer_id = serializers.SerializerMethodField()

    def get_cart_offer_id(self, obj):
        """
        Get the cart offer id
        :param obj:
        :return:
        """
        if obj.cart_offer:
            return obj.cart_offer.id
        return None

    def get_attribute_title(self, obj):
        """
        Get the attribute name
        :param obj:
        :return:
        """
        if obj.attribute:
            return obj.attribute.title
        return None

    def get_has_free_shipping(self, obj):
        """
        Check if the cart has free shipping
        :param obj:
        :return:
        """
        obj.cart.refresh_from_db()
        return obj.cart.has_free_shipping

    class Meta:
        """
        Returned fields for CartItemSerializer
        """

        model = CartItem
        fields = [
            "id",
            "type",
            "title",
            "thumbnails",
            "quantity",
            "attribute",
            "attribute_title",
            "sale_price",
            "total_price",
            "has_free_shipping",
            "cart_offer_id",
        ]


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model
    Used for returning the cart to the frontend
    """

    class Meta:
        model = Cart
        fields = [
            "is_empty",
            "get_items_total",
            "get_total_price",
            "has_free_shipping",
        ]


class AddOrderItemToOrderSerializer(serializers.Serializer):
    """
    Serializer for adding an order item to the order
    """

    order_id = serializers.IntegerField(min_value=1, required=True)
    order_item_id = serializers.IntegerField(min_value=1, required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    tracking_code = serializers.CharField(max_length=100, required=True)
    promotion_price = serializers.IntegerField(min_value=1, required=True)


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model
    Used for returning the order to the frontend
    """

    thank_you_page_url = serializers.SerializerMethodField()

    def get_thank_you_page_url(self, obj):
        """
        Get the thank you page url
        :param obj:
        :return:
        """
        return obj.get_absolute_url()

    class Meta:
        model = Order
        fields = [
            "id",
            "subtotal_price",
            "total_price",
            "tracking_number",
            "thank_you_page_url",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model
    Used for returning the order items to the frontend
    """

    thumbnails = serializers.SerializerMethodField()
    order_subtotal = serializers.SerializerMethodField()
    order_total = serializers.SerializerMethodField()
    order_shipping_method = serializers.SerializerMethodField()

    def get_order_subtotal(self, obj):
        """
        Get the order subtotal
        :param obj:
        :return:
        """
        return obj.order.subtotal_price

    def get_order_total(self, obj):
        """
        Get the order total
        :param obj:
        :return:
        """
        return obj.order.total_price

    def get_order_shipping_method(self, obj):
        """
        Get the order shipping
        :param obj:
        :return:
        """
        return obj.order.get_shipping_method

    def get_thumbnails(self, obj):
        """
        Get the thumbnails for the order item
        :param obj:
        :return:
        """
        return obj.get_thumbnail_loops

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "type",
            "get_readable_name",
            "thumbnails",
            "quantity",
            "attribute",
            "price",
            "total_price",
            "order_subtotal",
            "order_total",
            "order_shipping_method",
        ]


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShippingDetails model
    Used for adding shipping details to the cart
    """

    full_name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(required=True)
    city = serializers.CharField(max_length=50, required=True)
    municipality = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    email = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        """
        Required fields for ShippingDetailsSerializer
        """

        model = ShippingDetails
        fields = ["full_name", "address", "city", "phone", "municipality", "email"]

    def validate(self, data):
        """
        Validate the full_name
        Split the full_name into first_name and last_name
        :param data: the data to be validated
        :return: validated data with the first_name and last_name
        """
        errors = {}
        try:
            data["first_name"], data["last_name"] = self.validate_and_set_name(
                data.get("full_name")
            )
        except ValueError as e:
            errors.update(e.args[0])

        try:
            data["phone"] = self.validate_and_set_phone_number(data.get("phone"))
        except ValueError as e:
            errors.update(e.args[0])

        try:
            data["city"] = self.validate_supported_city(data.get("city"))
        except ValueError as e:
            errors.update(e.args[0])

        try:
            data["municipality"] = self.validate_and_set_municipality(
                data.get("municipality")
            )
        except ValueError as e:
            errors.update(e.args[0])

        try:
            data["email"] = self.validate_and_set_email(data.get("email"))
        except ValueError as e:
            errors.update(e.args[0])

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def validate_and_set_name(self, value):
        """
        Validate the full name
        :param value: the full name to be validated
        :return: the validated first_name and last_name
        """
        if value:
            parts = value.split()
            # if len(parts) < 2:
            #     raise ValueError(
            #         {"full_name": "Ве молиме внесете го целото име и презиме"}
            #     )
            first_name = parts[0]
            if len(parts) == 1:
                last_name = ""
            else:
                last_name = "".join(parts[1:])
            return first_name, last_name
        else:
            raise ValueError({"full_name": "Ве молиме внесете го вашето име и презиме"})

    def validate_and_set_phone_number(self, value):
        """
        Validate the phone number
        :param value: the phone number to be validated
        :return: the validated phone number
        """

        if value:
            phone = "".join(filter(str.isdigit, value))
            length = len(phone)
            # if phone.startswith("07") and length != 9:
            #     raise ValueError({"phone": "Телефонскиот број е невалиден"})
            # elif phone.startswith("389") and length != 11:
            #     raise ValueError({"phone": "Телефонскиот број е невалиден"})
            # elif length < 9:
            #     raise ValueError({"phone": "Телефонскиот број е невалиден"})

            if length == 0:
                raise ValueError({"phone": "Телефонскиот број е невалиден"})

            return phone

        else:
            raise ValueError({"phone": "Ве молиме внесете го телефонскиот број"})

    def validate_supported_city(self, value):
        """
        Validate the city
        :param value: the city in Latin to be validated
        :return: the validated city in Cyrillic
        """
        if not value or value == "":
            raise ValueError({"city": "Полето град е задолжително поле"})

        return value

        # # Create a dictionary to map Latin names to Cyrillic names for cities
        # latin_to_cyrillic = {c["latin"]: c["cyrillic"] for c in SUPPORTED_CITIES}
        #
        # # Retrieve the Cyrillic name using the provided Latin name
        # city_cyrillic = latin_to_cyrillic.get(value)
        # if not city_cyrillic:
        #     raise ValueError({"city": "Одберете го вашиот град од листата"})
        #
        # return city_cyrillic

    def validate_and_set_municipality(self, value):
        return None

        # """
        # Validate the municipality
        # :param value: the municipality to be validated
        # :return: the validated municipality
        # """
        # if not value or value == "":
        #     return None
        #
        # # Create a dictionary to map Latin names to Cyrillic names
        # latin_to_cyrillic = {
        #     m["latin"]: m["cyrillic"] for m in SUPPORTED_MUNICIPALITIES
        # }
        #
        # # Check if the provided Latin name is in the dictionary
        # municipality_cyrillic = latin_to_cyrillic.get(value)
        # if not municipality_cyrillic:
        #     raise ValueError({"municipality": "Одберете ја вашата општина од листата"})
        #
        # return municipality_cyrillic

    def validate_and_set_email(self, value):
        """
        Validate the email
        :param value: the email to be validated
        :return: the validated email
        """
        if not value or value == "":
            return None

        return value


class AbandonedCartDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the AbandonedCartDetails model
    """

    full_name = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=100
    )
    phone = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=100
    )
    city = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=100
    )
    email = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=100
    )
    address = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=100
    )

    class Meta:
        model = AbandonedCartDetails
        fields = ["full_name", "city", "phone", "email", "address"]
