import json
import urllib.parse
import uuid
from datetime import datetime
from hashlib import sha256

from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.delivery_category import DeliveryCategory
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData

from common.utils import get_ip_addr, get_user_agent
from facebook.services.api_connection import FacebookApi


class FacebookPixel:
    def __init__(self, request):
        self.fb_api = FacebookApi()
        self.request = request
        self.brand_name = "Trendiko"

    def view_content(self, product):
        if self.is_opted_in() is False:
            return

        user_data = self.get_default_user_data()
        content = Content(
            product_id=product.id,
            quantity=1,
            brand=self.brand_name,
            item_price=product.sale_price,
            delivery_category=DeliveryCategory.HOME_DELIVERY,
        )
        custom_data = CustomData(
            contents=[content],
            value=product.sale_price,
            currency="MKD",
            content_name=product.title,
            content_ids=[product.id],
            content_type="product",
        )
        event_0 = Event(
            event_name="ViewContent",
            event_time=int(datetime.now().timestamp()),
            user_data=user_data,
            custom_data=custom_data,
            action_source=ActionSource.WEBSITE,
            event_source_url=self.extract_event_source_url(),
            event_id=uuid.uuid4().hex,
        )

        events = [event_0]
        event_request = EventRequest(
            events=events,
            pixel_id=self.fb_api.dataset_id,
            access_token=self.fb_api.access_token,
            appsecret=self.fb_api.app_secret,
        )
        event_response = event_request.execute()

    def add_to_cart(
            self,
            cart_item,
    ):
        if self.is_opted_in() is False:
            return

        user_data = self.get_default_user_data()

        content = Content(
            product_id=self.extract_product_id(cart_item),
            quantity=cart_item.quantity,
            brand=self.brand_name,
            item_price=cart_item.sale_price,
            delivery_category=DeliveryCategory.HOME_DELIVERY,
        )

        custom_data = CustomData(
            contents=[content],
            value=cart_item.total_price,
            currency="MKD",
            content_name=cart_item.title,
            content_ids=[self.extract_product_id(cart_item)],
            content_type="product",
            delivery_category=DeliveryCategory.HOME_DELIVERY,
        )
        event = Event(
            event_name="AddToCart",
            event_time=int(datetime.now().timestamp()),
            user_data=user_data,
            custom_data=custom_data,
            action_source=ActionSource.WEBSITE,
            event_source_url=self.extract_event_source_url(),
            event_id=uuid.uuid4().hex,
        )

        events = [event]

        event_request = EventRequest(
            events=events,
            pixel_id=self.fb_api.dataset_id,
            access_token=self.fb_api.access_token,
            appsecret=self.fb_api.app_secret,
            test_event_code="TEST22283",
        )

        event_response = event_request.execute()

    def checkout(self, cart):
        if self.is_opted_in() is False:
            return

        user_data = self.get_default_user_data()
        content_ids = [
            self.extract_product_id(cart_item) for cart_item in cart.cart_items.all()
        ]
        custom_data = CustomData(
            value=cart.get_items_total,
            currency="MKD",
            content_type="product",
            num_items=cart.get_total_quantity,
            content_ids=content_ids,
            contents=[
                Content(
                    product_id=self.extract_product_id(cart_item),
                    quantity=cart_item.quantity,
                    item_price=cart_item.sale_price,
                    title=cart_item.title,
                )
                for cart_item in cart.cart_items.all()
            ],
        )

        event = Event(
            event_name="InitiateCheckout",
            event_time=int(datetime.now().timestamp()),
            user_data=user_data,
            custom_data=custom_data,
            action_source=ActionSource.WEBSITE,
            event_source_url=self.extract_event_source_url(),
            event_id=uuid.uuid4().hex,
        )

        events = [event]
        event_request = EventRequest(
            events=events,
            pixel_id=self.fb_api.dataset_id,
            access_token=self.fb_api.access_token,
            appsecret=self.fb_api.app_secret,
            test_event_code="TEST22283",
        )
        event_response = event_request.execute()

    def purchase(self, order):
        if self.is_opted_in() is False:
            return
        user_data = self.get_purchase_user_data(order.shipping_details)
        content_ids = [
            self.extract_product_id(order_item)
            for order_item in order.order_items.all()
        ]
        custom_data = CustomData(
            value=order.total_price,
            currency="MKD",
            content_type="product",
            num_items=order.get_total_quantity,
            content_ids=content_ids,
            contents=[
                Content(
                    product_id=self.extract_product_id(order_item),
                    quantity=order_item.quantity,
                    item_price=order_item.price,
                    title=order_item.get_readable_name,
                )
                for order_item in order.order_items.all()
            ],
        )

        event = Event(
            event_name="Purchase",
            event_time=int(datetime.now().timestamp()),
            user_data=user_data,
            custom_data=custom_data,
            action_source=ActionSource.WEBSITE,
            event_source_url=self.extract_event_source_url(),
            event_id=uuid.uuid4().hex,
        )

        events = [event]
        event_request = EventRequest(
            events=events,
            pixel_id=self.fb_api.dataset_id,
            access_token=self.fb_api.access_token,
            appsecret=self.fb_api.app_secret,
            test_event_code="TEST22283",
        )
        event_response = event_request.execute()

    def extract_product_id(self, item):
        if item.attribute is not None:
            return f"{item.product.id}-{item.attribute.id}"
        return item.product.id

    def extract_event_source_url(self):
        referrer = self.request.META.get("HTTP_REFERER")
        if referrer:
            return referrer
        return self.request.build_absolute_uri()

    def get_default_user_data(self):
        user_data = UserData(
            country_codes=[
                "4c3b3284e206c3db72440736cfdbd185f0e61a3c7fd9f049987196b987d3d1ee"
            ],
            client_ip_address=get_ip_addr(self.request),
            client_user_agent=get_user_agent(self.request),
            fbc=self.request.COOKIES.get("_fbc"),
            fbp=self.request.COOKIES.get("_fbp"),
        )
        return user_data

    def get_purchase_user_data(self, shipping_details):
        user_data = self.get_default_user_data()

        user_data.first_name = sha256(shipping_details.first_name.encode()).hexdigest()
        user_data.last_name = sha256(shipping_details.last_name.encode()).hexdigest()
        user_data.city = sha256(shipping_details.city.encode()).hexdigest()
        user_data.phone = sha256(shipping_details.phone.encode()).hexdigest()

        if shipping_details.email:
            user_data.email = sha256(shipping_details.email.encode()).hexdigest()

        return user_data

    def is_opted_in(self):
        cc_cookie = self.request.COOKIES.get("cc_cookie", None)

        if cc_cookie:
            decoded_cookie = urllib.parse.unquote(cc_cookie)
            cookie_data = json.loads(decoded_cookie)

            return "marketing" in cookie_data.get("categories", [])

        return True
