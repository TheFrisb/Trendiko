import logging
from datetime import datetime, timedelta

from django.utils import timezone

from analytics.models import CampaignSummary
from cart.models import OrderItem
from facebook.services.api_connection import FacebookApi


def create_campaign_summaries():
    logging.info("Analytics cron job started")

    start_time, end_time = get_yesterday_time_ranges()

    fb_api = FacebookApi()
    total_ad_spend = fb_api.get_adspend_per_campaigns(start_time, end_time)
    ad_spend_per_campaign = {
        campaign["campaign_id"]: campaign["spend"]
        for campaign in fb_api.get_adspend_per_campaigns(start_time, end_time)
    }
    print(ad_spend_per_campaign)
    return
    summaries = CampaignSummary.objects.filter(campaign_id__isnull=False)

    for summary in summaries:
        start_time, end_time = get_yesterday_time_ranges()
        order_items = OrderItem.objects.filter(
            created_at__range=(start_time, end_time),
            product__facebook_campaigns__campaign_id=summary.campaign_id,
        ).prefetch_related("reserved_stock_items", "reserved_stock_items__import_item")
        summary.populate_entry(order_items)


def get_yesterday_time_ranges():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    start_time = datetime.combine(yesterday, datetime.min.time())
    end_time = datetime.combine(yesterday, datetime.max.time())

    return start_time, end_time
