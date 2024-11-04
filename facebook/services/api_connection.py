import logging
from datetime import datetime

import requests
from decouple import config
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

from common.models import FacebookAccessToken


class FacebookApi:
    def __init__(self):
        self.app_id = config("FACEBOOK_APP_ID")
        self.app_secret = config("FACEBOOK_APP_SECRET")
        self.access_token = self.get_access_token_from_db()
        self.ad_account_id = config("FACEBOOK_AD_ACCOUNT_ID")
        self.dataset_id = config("FACEBOOK_DATASET_ID")

        FacebookAdsApi.init(self.app_id, self.app_secret, self.access_token)
        self.ad_account = AdAccount(f"act_{self.ad_account_id}")

    def test_connection(self):
        ad_account = AdAccount(f"act_{self.ad_account_id}")
        campaigns = ad_account.get_campaigns()
        for campaign in campaigns:
            print(campaign)

    def get_total_adspend_for_time_range(
            self, start_date: datetime, end_date: datetime
    ):
        params = {
            "time_range": {
                "since": start_date.strftime("%Y-%m-%d"),
                "until": end_date.strftime("%Y-%m-%d"),
            },
            "fields": ["spend"],
            "level": "account",
        }

        return self.ad_account.get_insights(params=params)

    def get_adspend_per_campaigns(self, start_date: datetime, end_date: datetime):
        params = {
            "time_range": {
                "since": start_date.strftime("%Y-%m-%d"),
                "until": end_date.strftime("%Y-%m-%d"),
            },
            "fields": ["campaign_id", "spend"],
            "level": "campaign",
        }
        return self.ad_account.get_insights(params=params)

    def refresh_access_token(self):
        """
        Refreshes the Facebook access token and updates it in the environment if needed.
        """
        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": self.access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            new_token = response.json().get("access_token")
            self.access_token = new_token
            FacebookAdsApi.init(self.app_id, self.app_secret, self.access_token)

            # Save the new token in the database
            FacebookAccessToken.objects.create(token=new_token)

            logging.info(f"Access token refreshed. New token: {new_token}")
        else:
            logging.error("Failed to refresh access token.")
            logging.error(response.text)

    def get_access_token_from_db(self):
        # Fetch the most recent access token from the database
        token_obj = FacebookAccessToken.objects.order_by("-id").first()
        if token_obj:
            return token_obj.token
        else:
            raise ValueError("Facebook access token not found in database.")
