from datetime import datetime

from decouple import config
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


class FacebookApi:
    def __init__(self):
        self.app_id = config("FACEBOOK_APP_ID")
        self.app_secret = config("FACEBOOK_APP_SECRET")
        self.access_token = config("FACEBOOK_ACCESS_TOKEN")
        self.pixel_access_token = config("FACEBOOK_PIXEL_ACCESS_TOKEN")
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
