from rest_framework.exceptions import APIException


class OutOfStockException(APIException):
    status_code = 403
    default_detail = "Requested quantity is more than available quantity"
    default_code = "out_of_stock"

    def __init__(self, requested_quantity, available_quantity, extraDict=None):
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity
        self.detail = {
            "requested_quantity": self.requested_quantity,
            "available_quantity": self.available_quantity,
        }

        if extraDict is not None:
            self.detail.update(extraDict)

        super().__init__(detail=self.detail, code=self.default_code)
