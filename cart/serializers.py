from rest_framework import serializers

from shop.models import Product
from .models import CartItem, ShippingDetails, Cart, Order


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

    def get_has_free_shipping(self, obj):
        """
        Check if the cart has free shipping
        :param obj:
        :return:
        """
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
            "sale_price",
            "total_price",
            "has_free_shipping",
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
            "get_total_quantity",
            "has_free_shipping",
        ]


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


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShippingDetails model
    Used for adding shipping details to the cart
    """

    full_name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=12, required=True)

    class Meta:
        """
        Required fields for ShippingDetailsSerializer
        """

        model = ShippingDetails
        fields = ["full_name", "address", "city", "phone"]

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
            print(e.args[0])
            errors.update(e.args[0])

        try:
            data["phone"] = self.validate_and_set_phone_number(data.get("phone"))
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
            if len(parts) < 2:
                raise ValueError(
                    {"full_name": "Ве молиме внесете го целото име и презиме"}
                )
            first_name = parts[0]
            last_name = " ".join(parts[1:])
            return first_name, last_name
        else:
            raise ValueError({"full_name": "Ве молиме внесете го целото име и презиме"})

    def validate_and_set_phone_number(self, value):
        """
        Validate the phone number
        :param value: the phone number to be validated
        :return: the validated phone number
        """

        if value:
            phone = "".join(filter(str.isdigit, value))
            length = len(phone)
            if phone.startswith("07") and length != 9:
                raise ValueError({"phone": "Телефонскиот број е невалиден"})
            elif phone.startswith("389") and length != 11:
                raise ValueError({"phone": "Телефонскиот број е невалиден"})
            elif length < 9:
                raise ValueError({"phone": "Телефонскиот број е невалиден"})
            return phone

        else:
            raise ValueError({"phone": "Ве молиме внесете го телефонскиот број"})
