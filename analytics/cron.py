import logging
from datetime import datetime, timedelta

from django.utils import timezone

from analytics.models import CampaignSummary
from cart.models import OrderItem
from facebook.services.api_connection import FacebookApi


def create_campaign_summaries():
    logging.info("Analytics cron job started")

    start_time, end_time = get_yesterday_time_ranges()

    logging.info(
        "Fetching ad spend per campaign for dates %s - %s", start_time, end_time
    )

    fb_api = FacebookApi()
    ad_spend_per_campaign = {
        campaign["campaign_id"]: float(campaign["spend"])
        for campaign in fb_api.get_adspend_per_campaigns(start_time, end_time)
    }
    logging.info("Fetched ad spend per campaign: %s", ad_spend_per_campaign)

    summaries = CampaignSummary.objects.filter(
        campaign_id__in=ad_spend_per_campaign.keys()
    )
    logging.info("Found %s summaries", summaries.count())

    for summary in summaries:
        logging.info("Processing summary for campaign %s", summary.campaign_id)

        order_items = OrderItem.objects.filter(
            created_at__range=(start_time, end_time),
            product__facebook_campaigns__campaign_id=summary.campaign_id,
        ).prefetch_related(
            "reserved_stock_items",
            "reserved_stock_items__import_item",
            "stock_item",
            "product",
        )
        logging.info("Found %s order items", order_items.count())

        summary.populate_entry(order_items)


def get_yesterday_time_ranges():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    start_time = datetime.combine(yesterday, datetime.min.time())
    end_time = datetime.combine(yesterday, datetime.max.time())

    return start_time, end_time
