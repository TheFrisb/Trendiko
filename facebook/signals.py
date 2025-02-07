# when facebookCampaign is created, create a CampaignSummary

from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import CampaignSummary
from facebook.models import FacebookCampaign


@receiver(post_save, sender=FacebookCampaign)
def create_campaign_summary(sender, instance, created, **kwargs):
    if created:
        CampaignSummary.objects.create(
            name=instance.product.title,
            product=instance.product,
            campaign_id=instance.campaign_id,
        )

    else:
        # Update the campaign id if it has changed
        summary = CampaignSummary.objects.get(product=instance.product)
        summary.campaign_id = instance.campaign_id
        summary.save()