from rest_framework import serializers

from shop.models import Product
from .models import CartItem, ShippingDetails


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
            "price",
            "total_price",
        ]


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the ShippingDetails model
    Used for adding shipping details to the cart
    """

    full_name = serializers.CharField(max_length=100, required=True)

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
        full_name = data.get("full_name")
        if full_name:
            parts = full_name.split()
            if len(parts) < 2:
                raise serializers.ValidationError("Please enter your full name")

            data["first_name"] = parts[0]

            if len(parts) > 2:
                data["last_name"] = " ".join(parts[1:])
            else:
                data["last_name"] = parts[1]

        return data
