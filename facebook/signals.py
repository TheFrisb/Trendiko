# when facebookCampaign is created, create a CampaignSummary

from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import CampaignSummary
from facebook.models import FacebookCampaign


@receiver(post_save, sender=FacebookCampaign)
def create_campaign_summary(sender, instance, created, **kwargs):
    if created:
        print("Creating Campaign Summary")
        CampaignSummary.objects.create(
            name="PLACEHOLDER",
            product=instance.product,
            campaign_id=instance.campaign_id,
        )
