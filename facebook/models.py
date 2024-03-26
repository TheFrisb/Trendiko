from django.db import models

from common.models import TimeStampedModel


# Create your models here.
class FacebookCampaign(TimeStampedModel):
    product = models.ForeignKey(
        "shop.Product", on_delete=models.CASCADE, related_name="facebook_campaigns"
    )
    campaign_id = models.CharField(
        max_length=255, unique=True, verbose_name="Campaign ID"
    )

    def __str__(self):
        return f"[{self.campaign_id}] {self.product.title}"
