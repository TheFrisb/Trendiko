from django.contrib import admin

from analytics.models import CampaignSummary, CampaignEntry


# Register your models here.
@admin.register(CampaignSummary)
class CampaignSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(CampaignEntry)
class CampaignEntryAdmin(admin.ModelAdmin):
    pass
