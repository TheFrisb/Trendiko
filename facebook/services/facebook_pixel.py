import uuid
from datetime import datetime

from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData

from facebook.services.api_connection import FacebookApi


class FacebookPixel:
    def __init__(self, request):
        self.fb_api = FacebookApi()
        self.request = request

    def view_content(self, product):
        user_data = UserData(
            country_codes=[
                "4c3b3284e206c3db72440736cfdbd185f0e61a3c7fd9f049987196b987d3d1ee"
            ],
            client_ip_address=self.request.META.get("REMOTE_ADDR"),
            client_user_agent=self.request.META.get("HTTP_USER_AGENT"),
        )
        custom_data = CustomData(
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

    def add_to_cart(self, product):
        user_data = UserData(
            country_codes=[
                "4c3b3284e206c3db72440736cfdbd185f0e61a3c7fd9f049987196b987d3d1ee"
            ],
            client_ip_address=self.request.META.get("REMOTE_ADDR"),
            client_user_agent=self.request.META.get("HTTP_USER_AGENT"),
        )
        custom_data = CustomData(
            value=product.sale_price,
            currency="MKD",
            content_name=product.title,
            content_ids=[product.id],
            content_type="product",
        )
        event = Event(
            event_name="AddToCart",
            event_time=int(datetime.now().timestamp()),
            user_data=user_data,
            custom_data=custom_data,
            action_source=ActionSource.WEBSITE,
            event_id=uuid.uuid4().hex,
        )

        events = [event]
        event_request = EventRequest(
            events=events,
            pixel_id=self.fb_api.dataset_id,
            access_token=self.fb_api.access_token,
            appsecret=self.fb_api.app_secret,
        )
        event_response = event_request.execute()
