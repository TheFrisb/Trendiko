# when facebookCampaign is created, create a CampaignSummary
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import CampaignSummary
from facebook.models import FacebookCampaign

logger = logging.getLogger(__name__)

@receiver(post_save, sender=FacebookCampaign)
def create_campaign_summary(sender, instance, created, **kwargs):
    if created:
        logger.info("Creating CampaignSummary for FacebookCampaign %s, product", instance, instance.product)
        CampaignSummary.objects.create(
            name=instance.product.title,
            product=instance.product,
            campaign_id=instance.campaign_id,
        )

    else:
        logger.info("Updating CampaignSummary for FacebookCampaign %s, product", instance, instance.product)
        summary = CampaignSummary.objects.get(product=instance.product)
        summary.campaign_id = instance.campaign_id
        summary.save()
