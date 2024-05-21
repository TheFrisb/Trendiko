import logging
from datetime import datetime, timedelta

from django.utils import timezone

from analytics.models import CampaignSummary
from cart.models import OrderItem, Order
from common.utils import get_euro_value_in_mkd
from facebook.services.api_connection import FacebookApi
from stock.models import ReservedStockItem, Import


def create_campaign_summaries(start_time: datetime = None, end_time: datetime = None):
    logging.info("Analytics cron job started")

    if not start_time or not end_time:
        start_time, end_time = get_yesterday_time_ranges()

    euro_to_mkd = get_euro_value_in_mkd()

    logging.info(
        "Fetching ad spend per campaign for dates %s - %s", start_time, end_time
    )

    fb_api = FacebookApi()
    ad_spend_per_campaign = {
        campaign["campaign_id"]: {
            "spend_eur": float(campaign["spend"]),
            "spend_mkd": float(campaign["spend"]) * euro_to_mkd,
        }
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
            order__status__in=[Order.OrderStatus.CONFIRMED, Order.OrderStatus.PENDING],
        ).prefetch_related(
            "reserved_stock_items",
            "reserved_stock_items__import_item",
            "stock_item",
            "product",
        )
        logging.info("Found %s order items", order_items.count())

        summary.populate_entry(
            order_items, ad_spend_per_campaign[summary.campaign_id], start_time
        )

    populate_imports_ad_spend(ad_spend_per_campaign, start_time, end_time)


def populate_imports_ad_spend(
    ad_spend_per_campaign: dict, start_time: datetime, end_time: datetime
):
    logging.info("Populating ad spend for imports")
    # loop over dict getting key and value
    imports_to_save = {}
    for campaign_id, ad_spend_data in ad_spend_per_campaign.items():
        reserved_stock_items = ReservedStockItem.objects.filter(
            created_at__range=(start_time, end_time),
            product__facebook_campaigns__campaign_id=campaign_id,
            order__status__in=[Order.OrderStatus.CONFIRMED, Order.OrderStatus.PENDING],
        ).prefetch_related("import_item", "import_item__parentImport")
        print(reserved_stock_items)
        updated_imports = set()

        for reserved_stock_item in reserved_stock_items:
            import_id = reserved_stock_item.import_item.parentImport.id
            if import_id not in imports_to_save:
                imports_to_save[import_id] = {
                    "ad_spend": 0,
                }

            if import_id not in updated_imports:
                imports_to_save[import_id]["ad_spend"] += ad_spend_data["spend_mkd"]
                updated_imports.add(import_id)

    for import_id, data in imports_to_save.items():
        import_item = Import.objects.get(id=import_id)
        import_item.ad_spend += data["ad_spend"]
        import_item.save()


def get_yesterday_time_ranges():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    start_time = datetime.combine(yesterday, datetime.min.time())
    end_time = datetime.combine(yesterday, datetime.max.time())

    return start_time, end_time


def create_campaign_summaries_for_time_range(start_date: datetime, end_date: datetime):
    current_date = start_date
    while current_date <= end_date:
        start_time = datetime.combine(current_date, datetime.min.time())
        end_time = datetime.combine(current_date, datetime.max.time())
        print(start_time, end_time)
        create_campaign_summaries(start_time, end_time)
        start_time += timedelta(days=1)
